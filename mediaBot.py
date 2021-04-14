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

bot = commands.Bot(command_prefix = prefix)

@bot.command()
async def follow(ctx, *args):
    await botCommands.followChannels(ctx, args)

@bot.command()
async def sudo(ctx, arg):
    if arg == "exit" or arg == "stop":
        await ctx.send("Sleep mode activated...")
        await bot.close()
        sys.exit()

bot.run(botToken)
