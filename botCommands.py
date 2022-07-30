# Python Modules
import sqlite3
# Third-Party Modules
import discord
# Custom Modules
import database

curs = database.conn.cursor()

# Add all the text channel IDs to a SQLite database
async def followChannels(ctx, args):
    # If the user specifies 'all' then all the text channels in the server are
    # added to the database
    guildID = ctx.guild.id
    if args[0].lower() == "all":
        channels = ctx.guild.text_channels
    for channel in channels:
        insertCommand = """INSERT INTO followedChannels
        (rowID, channelID, guildID) VALUES
        (NULL, ?, ?)"""
        curs.execute(insertCommand, (channel.id, guildID,))
    database.conn.commit()
    await ctx.send(f"Added **{len(channels)} channels** to the database")

# Get a list of all the links in a given channel; takes a channel object and
# returns a list of strings.
async def getLinks(channel):
    links = []
    async for message in channel.history():
        # If the message starts with "http" it's highly likely it's a link
        if message.content.startswith("http"):
            links.append(message.content)
    return links

# Scrapes all the followed channels in the given guild for links and appends or
# overwrites the database with them.
async def scrapeContent(ctx, args):
    # Get a list of all the channel IDs that the bot is following for the given
    # guild
    channelIDsCommand = "SELECT channelID FROM followedChannels WHERE guildID=?"
    curs.execute(channelIDsCommand, (ctx.guild.id,))
    # Returns a list of SQLite3 Row instances thanks to the row factory
    sqlRows = curs.fetchall()
    linksAdded = 0
    if args[0].lower() == "append":
        for row in sqlRows:
            channel = ctx.guild.get_channel(row["channelID"])
            links = await getLinks(channel)
            linksAdded += len(links)
            # Get the name of the category the channel is in and the name of the
            # channel itself; lowercase it for standardization purposes
            channelCategory = channel.category.name.lower()
            channelName = channel.name.lower()
            for link in links:
                insertCommand = """INSERT INTO links
                (rowID, channelCategory, channelName, guildID, link) VALUES
                (NULL, ?, ?, ?, ?)"""
                curs.execute(insertCommand,
                             (channelCategory, channelName, ctx.guild.id, link,))
            database.conn.commit()
        await ctx.send(f"Appended **{linksAdded} links** to the database")
