import sqlite3

conn = sqlite3.connect("books.sqlites")

cursor = conn.cursor()

sql_query = """ CREATE TABLE if not exists book (
    id integer PRIMARY KEY,
    author text,
    language text,
    title text
)"""

cursor.execute(sql_query)
