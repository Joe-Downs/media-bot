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

# Creates the table of links the bot stores; stores the channel group name, the
# channel name, and the link itself.
createLinksTable = """CREATE TABLE links (
rowID INTEGER PRIMARY KEY AUTOINCREMENT,
channelGroup TEXT,
channelName TEXT,
link TEXT)"""

# Creates the table of channels the bot is to follow; stores both the channel ID
# and the guild ID
createFollowTable = """CREATE TABLE followedChannels (
rowID INTEGER PRIMARY KEY AUTOINCREMENT,
channelID INTEGER,
guildID INTEGER)"""

# If an error is raised, the tables (hopefully) already exist; notify the user
# of this and continue.
try:
    curs.execute(createLinksTable)
except sqlite3.OperationalError as error:
    print(error)

try:
    curs.execute(createFollowTable)
except sqlite3.OperationalError as error:
    print(error)

conn.commit()
curs.close()


