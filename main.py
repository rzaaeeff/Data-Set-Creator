import os
import sqlite3
from sqlite3 import Error


class Letter:
    def __init__(self, author, letter, image, drawn_in_free_mode):
        self.author = author
        self.letter = letter
        self.image = image
        self.drawn_in_free_mode = drawn_in_free_mode


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_letters(conn):
    """
    Query all rows in the letters table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM letters;")

    return cur.fetchall()


def drop_table(conn):
    conn.cursor().execute(
        "DROP TABLE IF EXISTS letters;"
    )

def create_table(conn):
    conn.cursor().execute(
        "CREATE TABLE IF NOT EXISTS letters ("
        "id INTEGER PRIMARY KEY,"
        "author TEXT NOT NULL,"
        "letter TEXT NOT NULL,"
        "image BLOB NOT NULL,"
        "drawn_in_free_mode TINYINT NOT NULL"
        ");"
    )


def insert_all_letters(conn, letters):
    cur = conn.cursor()
    for letter_item in letters:
        cur.execute("INSERT INTO letters(author, letter, image, drawn_in_free_mode) values(?, ?, ?, ?);",
                    (letter_item.author,
                     letter_item.letter,
                     letter_item.image,
                     letter_item.drawn_in_free_mode))

    conn.commit()


# opening input folder
input_folder_path = "input"
input_folder_contents = os.listdir(input_folder_path)
databases = []

for filename in input_folder_contents:
    databases.append(input_folder_path + "/" + filename)

# collecting letters
letters = []

for database in databases:
    parts = database.split("-")[1:6]
    author = "-".join(parts)
    conn = create_connection(database)
    rows = select_all_letters(conn)
    for row in rows:
        letter = row[1]
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
output_folder_path = "output"
os.makedirs(output_folder_path)
output_database = output_folder_path + "/" + "DataSetCreator.db"

conn = create_connection(output_database)
drop_table(conn)
create_table(conn)
insert_all_letters(conn, letters)

rows = select_all_letters(conn)
print(str(len(rows)) + " entries")

conn.close()

print(str(os.stat(output_database).st_size / 1024) + "KB")