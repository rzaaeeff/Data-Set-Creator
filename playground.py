import db
import image_processor
from constant import DB_RESULT
from letter import Letter

conn = db.create_connection(DB_RESULT)
counts = db.show_counts_of_all_letters(conn)
# sorted_counts = {}
#
# for key in sorted(counts.keys(), reverse=True):
#    if (counts[key] is not 0):
#        sorted_counts[key] = counts[key]
#
# print(sorted_counts)
# counts_without_zeros = {}
#
# for key in counts:
#     if (counts[key] is not 0):
#         counts_withoutZeros)

filtered_counts = {}

for key in counts:
    if (counts[key] is not 0):
        filtered_counts[key] = counts[key]

print(filtered_counts)

# rows = db.select_all_letters(conn)
# letter_objects = []
# malfunc_id = [9085, 9193, 16316, 16318, 16319, 16321, 17510]
#
# for row in rows:
#     id = row[0]
#     author = row[1]
#     letter = row[2]
#     image = row[3]
#     drawn_in_free_mode = 0
#     try:
#         drawn_in_free_mode = row[4]
#     except IndexError:
#         pass
#
#     if id not in malfunc_id:
#         continue
#
#     letter_object = Letter(author, letter, image, drawn_in_free_mode)
#     letter_object.id = id
#     letter_objects.append(letter_object)
#
# letter_object_results = image_processor.preprocess_images(letter_objects)
#
# for letter_object in letter_object_results:
#     image_processor.save_image(letter_object.image, str(letter_object.id) + '.png')