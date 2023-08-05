import sqlite3

conn = sqlite3.connect("library1.db")

cursor = conn.cursor()

query="""CREATE TABLE if not exists book_data
          ( book_name text not null,
            book_id integer PRIMARY KEY,
            author text,
            status text ,
            category text)"""

cursor.execute(query)