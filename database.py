# Python Modules
import sqlite3

# This file ensures that the database is created (or already exists) with all
# the necessary tables

conn = sqlite3.connect("media.db")
# The Row instance allows for the row returned by sqlite3 to be mapped by column
# name and index in a dictionary-like format. Additionally, "it
# supports...iteration, representation, equality testing and len()"
# (from https://docs.python.org/3/library/sqlite3.html#sqlite3.Row)
conn.row_factory = sqlite3.Row
curs = conn.cursor()

sqlCommand = f"""CREATE TABLE links (
rowID INTEGER PRIMARY KEY AUTOINCREMENT,
channelGroup TEXT,
channelName TEXT,
link TEXT)"""

try:
    curs.execute(sqlCommand)
except sqlite3.OperationalError as error:
    print(error)

conn.commit()
curs.close()


