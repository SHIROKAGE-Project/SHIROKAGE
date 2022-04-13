import discord
from discord.ext import commands

from os import environ,listdir

from dotenv import load_dotenv
import jishaku


load_dotenv()
TOKEN = environ["TOKEN"]

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="s!",intents=intents)

bot.load_extension("jishaku")

for cog in [cog[:-3] for cog in listdir("cogs") if cog.endswith(".py")]:
    bot.load_extension(f"cogs.{cog}")
#test
bot.run(TOKEN)