# This file is for getting all the Gfycat links from the database and using
# ShineAsNine's Gfycat downloader
# (https://github.com/ShineAsNine/GfycatDownloader) to save them to disk. This
# is in preparation of Gfycat shutting down on September 1, 2023.

import sqlite3
import config

dbName = config.getDatabaseName()

conn = sqlite3.connect(dbName)
conn.row_factory = sqlite3.Row
curs = conn.cursor()

gfycatLinksSQL = """SELECT channelCategory, channelName, link
FROM links WHERE link LIKE '%gfycat%' ORDER BY channelCategory;"""

curs.execute(gfycatLinksSQL)
