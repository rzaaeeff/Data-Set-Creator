from PIL import Image
import io
import multiprocessing as mp
from joblib import Parallel, delayed
from tqdm import tqdm

__LEFT, __TOP, __RIGHT, __BOTTOM = 0, 1, 2, 3
__PADDING = 10

def find_edges(image):
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


def add_padding(edges, padding=__PADDING):
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


def squarify(edges):
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


def calculate_width_height_average(images):
    """
    Parallel execution to calculate width and height average
    :param images: list of PIL images
    :return:
    """
    results = Parallel(n_jobs=mp.cpu_count())(
        delayed(get_size_after_processing)(image) for image in tqdm(images))

    width_sum, height_sum = 0, 0

    for result in results:
        width_sum += result[0]
        height_sum += result[1]

    print(width_sum, height_sum)

    return width_sum // len(results), height_sum // len(results)


def get_size_after_processing(image):
    image = Image.open(io.BytesIO(image))
    nimage = Image.new("RGB", image.size, "WHITE")
    nimage.paste(image, (0, 0), image)
    nimage.convert('LA')

    edges = find_edges(nimage)
    add_padding(edges)
    squarify(edges)
    width = edges[__RIGHT] - edges[__LEFT]
    height = edges[__BOTTOM] - edges[__TOP]

    # print('\r' + str(len(widths)), end='')
    return width, height