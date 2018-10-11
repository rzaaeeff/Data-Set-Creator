import os
from db import *

class Letter:
    def __init__(self, author, letter, image, drawn_in_free_mode):
        self.author = author
        self.letter = letter
        self.image = image
        self.drawn_in_free_mode = drawn_in_free_mode

def convert_if_similar(letter):
    similar_letters = ['Ə', 'Ş', 'Ç', 'Ü', 'Ö', 'C', 'S', 'O', 'U', 'V', 'X', 'Z', 'K']

    for element in similar_letters:
        if element == letter:
            return letter.lower()

    return letter

# opening input folder
input_folder_contents = os.listdir(INPUT_FOLDER)
databases = []

for filename in input_folder_contents:
    databases.append(INPUT_FOLDER + "/" + filename)

# collecting letters
letters = []

for database in databases:
    parts = database.split("-")[1:6]
    author = "-".join(parts)
    conn = create_connection(database)
    rows = select_all_letters(conn)
    for row in rows:
        letter = convert_if_similar(row[1])

        # ignore 'w' & 'W'
        if letter == 'w' or letter == 'W':
            continue

        image = row[2]
        drawn_in_free_mode = 0
        try:
            drawn_in_free_mode = row[3]
        except IndexError:
            pass

        letters.append(Letter(author, letter, image, drawn_in_free_mode))

    if len(rows) == 0:
        # indicate empty db
        print(database + " is empty!")
    conn.close()


# creating or opening output db file
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

conn = create_connection(DATABASE)
drop_table(conn)
create_table(conn)
insert_all_letters(conn, letters)

rows = select_all_letters(conn)
print(str(len(rows)) + " entries")

conn.close()

print(str(os.stat(DATABASE).st_size / 1024) + "KB")
