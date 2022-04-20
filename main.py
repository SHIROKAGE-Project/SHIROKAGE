import discord
from discord.ext import commands

from os import environ,listdir

from dotenv import load_dotenv
import jishaku


load_dotenv()
TOKEN = environ["TOKEN"]

intents = discord.Intents.default()

<<<<<<< HEAD
bot = commands.Bot(command_prefix="sc!",intents=intents,help_command=None)
=======
bot = commands.Bot(command_prefix="s!",intents=intents)
>>>>>>> be9398d0baf9d453ae8081ec0415f591105332d0

bot.load_extension("jishaku")

for cog in [cog[:-3] for cog in listdir("cogs") if cog.endswith(".py")]:
    bot.load_extension(f"cogs.{cog}")
#test
bot.run(TOKEN)