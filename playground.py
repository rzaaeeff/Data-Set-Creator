import db

conn = db.create_connection(db.DATABASE)
counts = db.show_counts_of_all_letters(conn)

print(counts)