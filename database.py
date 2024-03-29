# Python Modules
import sqlite3
from datetime import datetime
# Custom Modules
import config

# This file ensures that the database is created (or already exists) with all
# the necessary tables

dbName = config.getDatabaseName()

conn = sqlite3.connect(dbName)
# The Row instance allows for the row returned by sqlite3 to be mapped by column
# name and index in a dictionary-like format. Additionally, "it
# supports...iteration, representation, equality testing and len()"
# (from https://docs.python.org/3/library/sqlite3.html#sqlite3.Row)
conn.row_factory = sqlite3.Row
curs = conn.cursor()

# Creates the table of links the bot stores; stores the channel category name,
# the channel name, and the link itself.
createLinksTable = """CREATE TABLE links (
rowID INTEGER PRIMARY KEY AUTOINCREMENT,
channelCategory TEXT,
channelName TEXT,
guildID INTEGER,
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


