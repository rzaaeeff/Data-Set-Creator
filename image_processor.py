from PIL import Image
import io
import multiprocessing as mp
from joblib import Parallel, delayed
from tqdm import tqdm

# these indexes are fixed, necessary for helper to work
# if you change them, adapt your code accordingly
__LEFT, __TOP, __RIGHT, __BOTTOM = 0, 1, 2, 3

__PADDING = 20

# sizes from initial dataset were averaged around 545
# which means that the average width and height was 545 pixels
# but this size is big for training and will slow down the entire process
# so I decided to use lower size which will also not affect the quality
# since the overall aspect ratio (square) is preserved...
__SIZE = 320

def __find_edges(image):
    """
    method returns edges from given image
    :param image: PIL image
    :return: left, top, right, bottom edges in order
    """
    pixels = image.load()
    width, height = image.size
    left, top, right, bottom = width - 1, height - 1, 0, 0
    for x in range(width):
        for y in range(height):
            if pixels[x, y][0] == 0:
                if top > y:     top = y
                if bottom < y:  bottom = y
                if left > x:    left = x
                if right < x:   right = x

    return [left, top, right, bottom]


def __add_padding(edges, padding=__PADDING):
    """
    Add defined padding to all edges
    :param padding:
    :param edges:
    :return:
    """
    edges[__LEFT] -= padding
    edges[__TOP] -= padding
    edges[__RIGHT] += padding
    edges[__BOTTOM] += padding

    return edges


def __squarify(edges):
    """
    Adjust edges to have square area
    :param edges:
    :return:
    """
    width = edges[__RIGHT] - edges[__LEFT]
    height = edges[__BOTTOM] - edges[__TOP]

    if width > height:
        diff = width - height
        edges[__TOP] -= diff / 2
        edges[__BOTTOM] += (diff - diff / 2)
    elif height > width:
        diff = height - width
        edges[__LEFT] -= diff / 2
        edges[__RIGHT] += (diff - diff / 2)

    return edges


def calculate_width_height_average(blobs):
    """
    Parallel execution to calculate width and height average
    :param blobs: list of images as binary objects
    :return: average width and height
    """
    results = Parallel(n_jobs=mp.cpu_count())(
        delayed(__get_size_after_processing)(__blob_to_image(blob)) for blob in tqdm(blobs))

    width_sum, height_sum = 0, 0

    for result in results:
        width_sum += result[0]
        height_sum += result[1]

    print(width_sum, height_sum)

    return width_sum // len(results), height_sum // len(results)


def preprocess_images(blobs):
    images = []
    for blob in blobs:
        images.append(__blob_to_image(blob))

    results = __preprocess_images(images)

    blob_results = []
    for result in results:
        blob_results.append(__image_to_blob(result))

    return blob_results

def __preprocess_images(images):
    """
    Parallel execution to preprocess images
    :param blobs: list of images as binary objects
    :return: list preprocess images as binary objects
    """
    return Parallel(n_jobs=mp.cpu_count())(
        delayed(__get_preprocessed_image)(image) for image in tqdm(images))


def __get_size_after_processing(image, padding=__PADDING):
    nimage = Image.new("RGB", image.size, "WHITE")
    nimage.paste(image, (0, 0), image)
    nimage.convert('LA')

    edges = __find_edges(nimage)
    edges = __add_padding(edges, padding)
    edges = __squarify(edges)
    width = edges[__RIGHT] - edges[__LEFT]
    height = edges[__BOTTOM] - edges[__TOP]

    # print('\r' + str(len(widths)), end='')
    return width, height

def __get_preprocessed_image(image, padding=__PADDING, size=__SIZE):
    nimage = Image.new("RGB", image.size, "WHITE")
    nimage.paste(image, (0, 0), image)
    nimage.convert('LA')

    edges = __find_edges(nimage)
    edges = __add_padding(edges, padding)
    edges = __squarify(edges)

    nimage = nimage.crop(edges)
    nimage = __square_resize(nimage, size)

    return nimage

def __square_resize(image, size):
    return image.resize((size, size))

def __blob_to_image(blob):
    return Image.open(io.BytesIO(blob))

def __image_to_blob(image):
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()

def show_image(blob):
    __blob_to_image(blob).show()

def save_image(blob, name):
    __blob_to_image(blob).save(name, 'PNG')