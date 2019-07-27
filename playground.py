import db
from constant import DB_RESULT

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