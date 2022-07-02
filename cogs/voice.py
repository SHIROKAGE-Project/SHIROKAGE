import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.voice = None

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("先にボイスチャンネルに接続してください")
            return
        self.voice = await ctx.author.voice.channel.connect()
        await ctx.send("接続しました")
    
    @commands.command()
    async def leave(self,ctx):
        if ctx.guild.voice_client is None:
            await ctx.send("ボイスチャンネルに接続していません")
            return
        await ctx.guild.voice_client.disconnect()
        await ctx.send("切断しました")
    
def setup(bot):
    return bot.add_cog(Voice(bot))