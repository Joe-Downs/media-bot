# This file is for getting all the Gfycat links from the database and using
# ShineAsNine's Gfycat downloader
# (https://github.com/ShineAsNine/GfycatDownloader) to save them to disk. This
# is in preparation of Gfycat shutting down on September 1, 2023.

import os
import sqlite3
import config

dbName = config.getDatabaseName()

conn = sqlite3.connect(dbName)
conn.row_factory = sqlite3.Row
curs = conn.cursor()

# Create the necessary folders (if they don't already exist) for the categories
# and names in the DB.
def createFolders():
    categoriesSQL = """SELECT DISTINCT channelCategory FROM Links;"""
    for categoryRow in curs.execute(categoriesSQL):
        categoryFolder = f"./downloaded/{categoryRow['channelCategory']}/"
        #print(f"Creating category folder: {categoryFolder}")
        if not os.path.exists(categoryFolder):
            os.makedirs(categoryFolder)

    categoryNameSQL = """SELECT DISTINCT channelCategory, channelName FROM links;"""
    for nameRow in curs.execute(categoryNameSQL):
        nameFolder = f"./downloaded/{nameRow['channelCategory']}/{nameRow['channelName']}/"
        #print(f"Creating name folder: {nameFolder}")
        if not os.path.exists(nameFolder):
            os.makedirs(nameFolder)

    # Remove any existing output files in the folders
    outputFile = f"{nameFolder}{nameRow['channelName']}.txt"
    if os.path.exists(outputFile):
        os.remove(outputFile)
    return

createFolders()

gfycatLinksSQL = """SELECT channelCategory, channelName, link
FROM links WHERE link LIKE '%gfycat%' ORDER BY channelCategory;"""

for entryRow in curs.execute(gfycatLinksSQL):
    #print(f"Category: {entryRow['channelCategory']} - Name: {entryRow['channelName']} - Link: {entryRow['link']}")
    outputFile = f"./downloaded/{entryRow['channelCategory']}/{entryRow['channelName']}/{entryRow['channelName']}.txt"
    with open(outputFile, 'a') as textFile:
        print(f"Writing to {outputFile}: {entryRow['link']}")
        textFile.write(f"{entryRow['link']}\n")
