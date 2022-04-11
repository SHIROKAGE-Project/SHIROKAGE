import discord
from discord.ext import commands

from os import environ
from dotenv import load_dotenv

import jishaku


load_dotenv()
TOKEN = environ["TOKEN"]

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="s!",intents=intents)

bot.load_extension("jishaku")

@bot.command()
async def test(ctx):
    await ctx.send("hey")

bot.run(TOKEN)