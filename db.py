import sqlite3
from sqlite3 import Error

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
DATABASE = OUTPUT_FOLDER + "/" + "DataSetCreator.db"

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


def show_counts_of_all_letters(conn):
    alphabet = "əƏğĞıIöÖşŞüÜaAbBcCçÇdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVxXyYzZ"
    counts = {}

    rows = select_all_letters(conn)

    for letter in alphabet:
        counts[letter] = show_count_of(letter, rows)

    return counts


def show_count_of(letter, conn):
    rows = select_all_letters(conn)

    return _show_count_of(letter, rows)


def _show_count_of(letter, rows):
    count = 0

    for row in rows:
        if row[2] == letter:
            count += 1

    return count