import db

conn = db.create_connection(db.DATABASE)
counts = db.show_counts_of_all_letters(conn)
sorted_counts = {}

for key in sorted(counts.keys(), reverse=True):
    sorted_counts[key] = counts[key]

print(sorted_counts)
