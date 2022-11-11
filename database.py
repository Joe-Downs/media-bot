# Python Modules
import sqlite3
from datetime import datetime
# Custom Modules
import config

# This file ensures that the database is created (or already exists) with all
# the necessary tables

# Get the custom database name from the config file, if there is one. If there
# is, always use that. If not, create a new database every time the bot starts
# up, giving it a timestamp.
dbName = config.getDatabaseName()

if len(dbName) == 0:
    nowDatetime = datetime.now()
    timestamp = nowDatetime.strftime("%y%m%d-%H%M%S")
    dbFilename = f"media-{timestamp}"
else:
    # Strip the extension if there is one, we'll add one. Since the user might
    # configure their filename without it.
    dbFilename = dbName.rstrip(".db")

conn = sqlite3.connect(f"{dbFilename}.db")
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


