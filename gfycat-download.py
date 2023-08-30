# This file is for getting all the Gfycat links from the database and using
# ShineAsNine's Gfycat downloader
# (https://github.com/ShineAsNine/GfycatDownloader) to save them to disk. This
# is in preparation of Gfycat shutting down on September 1, 2023.

import os
import sqlite3
import config
import sys
sys.path.append("./gfycat-downloader")
import commands.links_from_txt as links_from_txt

dbName = config.getDatabaseName()

conn = sqlite3.connect(dbName)
conn.row_factory = sqlite3.Row
curs = conn.cursor()

categoryNameSQL = """SELECT DISTINCT channelCategory, channelName FROM links;"""
gfycatLinksSQL = """SELECT channelCategory, channelName, link
FROM links WHERE link LIKE '%gfycat%' ORDER BY channelCategory;"""

# ================================== Functions =================================

# Create the necessary folders (if they don't already exist) for the categories
# and names in the DB.
def createFolders():
    categoriesSQL = """SELECT DISTINCT channelCategory FROM Links;"""
    for categoryRow in curs.execute(categoriesSQL):
        categoryFolder = f"./downloaded/{categoryRow['channelCategory']}/"
        #print(f"Creating category folder: {categoryFolder}")
        if not os.path.exists(categoryFolder):
            os.makedirs(categoryFolder)

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

# Write out the Gfycat links to text files in their respective folders
def writeTextFiles():
    for entryRow in curs.execute(gfycatLinksSQL):
        #print(f"Category: {entryRow['channelCategory']} - Name: {entryRow['channelName']} - Link: {entryRow['link']}")
        outputFile = f"./downloaded/{entryRow['channelCategory']}/{entryRow['channelName']}/{entryRow['channelName']}.txt"
        with open(outputFile, 'a') as textFile:
            print(f"Writing to {outputFile}: {entryRow['link']}")
            textFile.write(f"{entryRow['link']}\n")
    return

# Download the gfycat links in the text files
def downloadGfycats():
    for nameRow in curs.execute(categoryNameSQL):
        textFile = f"./downloaded/{nameRow['channelCategory']}/{nameRow['channelName']}/{nameRow['channelName']}.txt"
        outputDir = f"./downloaded/{nameRow['channelCategory']}/{nameRow['channelName']}/"
        print(f"Downloading from: {textFile}")
        links_from_txt.links_from_txt(outputDir, "%(upload_date)s - %(title)s [%(gfy_id)s]", textFile, "3", 5, False)
    return

# ==============================================================================

writeTextFiles()
createFolders()
downloadGfycats()
