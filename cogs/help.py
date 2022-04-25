import discord
from discord.ext import commands

class Help(commands.Cog):
    """このメッセージを表示します"""
    def __init__(self,bot):
        self.bot = bot
        self.cogdict = {name:item for name,item in dict(self.bot.cogs).items() if name != "Jishaku"}

    @commands.command()
    async def help(self,ctx,command=None):
        if command == None:

            def check(msg):
                return  msg.author == ctx.author and int(msg.content) in range(len(self.cogdict))

            cogpool = []
            for num,name in enumerate(self.cogdict.keys()):
                cogpool.append(f"{num} : `{name}`  {self.cogdict[name].description}")
            helpmsg = "\n".join(cogpool)
            await ctx.send(embed=discord.Embed(
                title="HELP",
                description="__詳細を確認したいカテゴリの番号を入力してください__\n\n"+helpmsg
            ))
            select = await self.bot.wait_for("message",check=check)

            #select_cog(cogname,cogobj)
            select_cog = list(self.cogdict.items())[int(select.content)]

            cmdlist = select_cog[1].get_commands()
            helpmsg = []
            for num,cmd in enumerate(cmdlist):
                helpmsg.append(f"{num} : `{cmd.name}`  {cmd.description}")
            helpmsgl = "\n".join(helpmsg)
            await ctx.send(embed=discord.Embed(
                title=f"{select_cog[0]}カテゴリのコマンドリスト",
                description=helpmsgl
            ))

            def check1(msg):
                return  msg.author == ctx.author and int(msg.content) in range(len(cmdlist))
            
            select = await self.bot.wait_for("message",check=check1)
            
            select_cmd = cmdlist[int(select.content)]
            await ctx.send(embed=discord.Embed(
                title=f"Help-{select_cmd.name}",
                description=select_cmd.help
            ))
            

def setup(bot):
    return bot.add_cog(Help(bot))