import os
import shutil

from tqdm import tqdm

import db
import image_processor
from constant import *

class Letter:
    def __init__(self, author, letter, image, drawn_in_free_mode, id=-1):
        self.id = id
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
print('\nCollecting letters from input databases...')
input_folder_contents = os.listdir(DB_INPUT_FOLDER)
databases = []

for filename in input_folder_contents:
    databases.append(DB_INPUT_FOLDER + '/' + filename)

# collecting letters
letters = []

print('\nInserting collected data to one output database...')
for database in databases:
    parts = database.split('-')[1:6]
    author = '-'.join(parts)
    conn = db.create_connection(database)
    rows = db.select_all_letters(conn)
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
        print(database + ' is empty!')
    conn.close()


# creating or opening output db file
os.makedirs(DB_OUTPUT_FOLDER, exist_ok=True)

conn = db.create_connection(DB_RESULT)
db.drop_table(conn)
db.create_table(conn)
db.insert_all_letters(conn, letters)

print('\nInsertion finished. Results are below:')
rows = db.select_all_letters(conn)
print(str(len(rows)) + ' entries')

print(str(os.stat(DB_RESULT).st_size / 1024) + 'KB')

# pre-processing data
# 1. getting letters from db
letter_objects = []

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
    letter_object.id = id
    letter_objects.append(letter_object)

print('\nPre-processing images...')
letter_object_results = image_processor.preprocess_images(letter_objects)

# 2. creating folders
print('\nCreating folders for preprocessed output...')
if os.path.exists(PREPROCESSED_OUTPUT_FOLDER) and os.path.isdir(PREPROCESSED_OUTPUT_FOLDER):
    shutil.rmtree(PREPROCESSED_OUTPUT_FOLDER)

os.makedirs(PREPROCESSED_OUTPUT_FOLDER, exist_ok=True)

for letter in tqdm(ALPHABET):
    if letter.isupper(): letter = '_' + letter
    os.makedirs(PREPROCESSED_OUTPUT_FOLDER + '/' + letter, exist_ok=True)

# 3. saving them
print('\nSaving pre-processed images')
for letter_object_result in tqdm(letter_object_results):
    letter = letter_object_result.letter
    blob = letter_object_result.image
    if letter.isupper():
        letter = '_' + letter
    image_processor.save_image(blob,
                               PREPROCESSED_OUTPUT_FOLDER +
                               '/' +
                               letter +
                               '/' + str(letter_object_result.id) +
                               '.png')
    
print('\nPre-processing finished.')