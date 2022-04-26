import discord
from discord.ext import commands

class Help(commands.Cog):
    """ヘルプ"""
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def help(self,ctx,command=None):
        """このメッセージを表示します
        
        __# 引数__
        コマンド名
        """
        if command == None:
            cogdict = {name:item for name,item in dict(self.bot.cogs).items() if name != "Jishaku"}
            
            def cog_check(msg):
                return  msg.author == ctx.author and int(msg.content) in range(len(cogdict))

            await ctx.send(embed=discord.Embed(
                title="Help",
                description="**詳細を知りたいカテゴリの番号を入力**\n\n"+"\n\n".join(f"{num} : `{name}`  {cogdict[name].description}" for num,name in enumerate(cogdict.keys())),
                color=0xffffff
            ))

            select = await self.bot.wait_for("message",check=cog_check)

            #select_cog(cogname,cogobj)
            select_cog = list(cogdict.items())[int(select.content)]
            cmdlist = select_cog[1].get_commands()

            await ctx.send(embed=discord.Embed(
                title=f"Help-{select_cog[0]}カテゴリのコマンドリスト",
                description="**詳細を知りたいコマンドの番号を入力**\n\n"+"\n\n".join(f"{num} : `{cmd.name}`  {str(cmd.help).split(maxsplit=1)[0]}" for num,cmd in enumerate(cmdlist)),
                color=0xffffff
            ))

            def cmd_check(msg):
                return  msg.author == ctx.author and int(msg.content) in range(len(cmdlist))
            
            select = await self.bot.wait_for("message",check=cmd_check)
            select_cmd = cmdlist[int(select.content)]

            await ctx.send(embed=discord.Embed(
                title=f"Help-{select_cmd.name}",
                description=select_cmd.help,
                color=0xffffff
            ))

        else:
            if command in [cmd.name for cmd in self.bot.commands]:
                cmd = self.bot.get_command(command)

                await ctx.send(embed=discord.Embed(
                    title=f"Help-{cmd.name}",
                    description=cmd.help,
                    color=0xffffff
                ))

            else:
                await ctx.send("コマンドが見つかりませんでした")

def setup(bot):
    return bot.add_cog(Help(bot))