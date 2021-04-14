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
        curs.execute(insertCommand, (guildID, channel.id,))
    database.conn.commit()
    await ctx.send(f"Added **{len(channels)} channels** to the database")
        
        
        
    
