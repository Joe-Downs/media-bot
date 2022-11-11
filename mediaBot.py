# Python Modules
import sys
# Third-Party Modules
import discord
from discord.ext import commands
# Custom Modules
import botCommands
import config

owner_ID = 174362561385332736
botToken = config.getToken()
prefix = config.getPrefix()

botIntents = discord.Intents.default()
botIntents.message_content = True

bot = commands.Bot(command_prefix = prefix, intents = botIntents)

@bot.command()
async def follow(ctx, *args):
    await botCommands.followChannels(ctx, args)

# Scrapes all the followed channels in the server for links to add to the
# database. Takes arguments for what to do with the links it scrapes (append or
# overwrite) the database.
@bot.command()
async def scrape(ctx, *args):
    await botCommands.scrapeContent(ctx, args)

@bot.command()
async def sudo(ctx, arg):
    if arg == "exit" or arg == "stop":
        await ctx.send("Sleep mode activated...")
        await bot.close()
        sys.exit()

bot.run(botToken)
