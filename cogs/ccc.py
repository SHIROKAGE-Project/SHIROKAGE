import discord
from discord.ext import commands

import re
import json

class CCC(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def ccc(self,ctx,message_id):
        flag = "失敗"
        async for message in ctx.channel.history(limit=300):
            if "sc!" in message.content or message.author.bot:
                continue
            try:
                num = re.search("[0-9]+",message.content)
                print(num)
                num = num.group()
                num = int(num)
                with open("data/data.json","r") as file:
                    f = json.load(file)
                if str(message.guild.id) not in f:
                    f[str(message.guild.id)] = {}
                if str(message.author.id) not in list(f.keys()):
                    f[str(message.guild.id)][str(message.author.id)] = 0
                f[str(message.guild.id)][str(message.author.id)] += num
                with open("data/data.json","w") as file:
                    json.dump(f,file,indent=4)
            except Exception as e:
                print(e)
                pass
            if message.id == int(message_id):
                flag = "成功"
                break
        await ctx.send(f"処理を完了しました\n目印としたメッセージの取得:{flag}")

def setup(bot):
    return bot.add_cog(CCC(bot))