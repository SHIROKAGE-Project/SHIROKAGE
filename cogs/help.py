import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cogdict = dict(self.bot.cogs)

    @commands.command()
    async def help(self,ctx,command=None):
        if command == None:
            def check(msg):
                return int(msg) in range(len(self.cogdict))  and msg.author == ctx.author
            cogpool = []
            for num,name in enumerate(self.cogdict.keys()):
                cogpool.append(f"{num} : {name}")
            helpmsg = "\n".join(cogpool)
            await ctx.send(embed=discord.Embed(
                title="HELP",
                description=helpmsg
            ))

def setup(bot):
    return bot.add_cog(Help(bot))