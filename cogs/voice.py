import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.voice = None

    @commands.command()
    async def connect(self,ctx):
        self.voice = await discord.VoiceChannel.connect(ctx.author.voice.channel)
    
    @commands.command()
    async def disconnect(self,ctx):
        await self.voice.disconnect()
    
def setup(bot):
    return bot.add_cog(Voice(bot))