import db
from main import Letter
import image_processor

conn = db.create_connection(db.DATABASE)
# counts = db.show_counts_of_all_letters(conn)
#sorted_counts = {}
#
#for key in sorted(counts.keys(), reverse=True):
#    if (counts[key] is not 0):
#        sorted_counts[key] = counts[key]
#
#print(sorted_counts)
# counts_without_zeros = {}
#
# for key in counts:
#     if (counts[key] is not 0):
#         counts_without_zeros[key] = counts[key]
#
# print(counts_without_zeros)
# filtered_counts = {}
#
# for key in counts:
#     if (counts[key] is not 0):
#         filtered_counts[key] = counts[key]
#
# print(filtered_counts)

rows = db.select_all_letters(conn)
id_letter_pair_list = []
count = 0

for row in rows:
    id = row[0]
    author = row[1]
    letter = row[2]
    image = row[3]
    drawn_in_free_mode = 0
    try:
        drawn_in_free_mode = row[4]
    except IndexError:
        pass

    letter_object = Letter(author, letter, image, drawn_in_free_mode)
    id_letter_pair_list.append((id, letter_object))

    count += 1
    if count == 3: break

blobs = []

for id, letter_object in id_letter_pair_list:
    blobs.append(letter_object.image)

blob_results = image_processor.preprocess_images(blobs)

for blob in blob_results:
    image_processor.save_image(blob, str(blob[1:40]) + '.png')