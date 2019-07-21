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
letter_objects = []
images = []

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

    letter_objects.append(Letter(author, letter, image, drawn_in_free_mode))
    images.append(image)

avg_width, avg_height = image_processor.calculate_width_height_average(images)
print(avg_width, avg_height)