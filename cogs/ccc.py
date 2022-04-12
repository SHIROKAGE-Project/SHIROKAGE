import discord
from discord.ext import commands

import re
import json

class CCC(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def ccc(self,ctx,message_id):
        """引数:トリガーとするメッセージID
        実行チャンネル内で数字の含まれるメッセージを取得し、ユーザー別に取得回数と数値の合計を集計します。
        取得するのはトリガーに設定したメッセージまでで、遡ることのできる上限は300件です。
        !のついたメッセージは無視されます。
        """
        flag = "失敗"
        async for message in ctx.channel.history(limit=300):
            if "!" in message.content or message.author.bot:
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
                if str(message.author.id) not in list(f[str(message.guild.id)].keys()):
                    f[str(message.guild.id)][str(message.author.id)] = {
                        "num":0,
                        "count":0
                    }
                f[str(message.guild.id)][str(message.author.id)]["num"] += num
                f[str(message.guild.id)][str(message.author.id)]["count"] += 1
                with open("data/data.json","w") as file:
                    json.dump(f,file,indent=4)
            except:
                pass
            if message.id == int(message_id):
                flag = "成功"
                break
        await ctx.send(f"処理を完了しました\nトリガーとしたメッセージの取得:{flag}")
    
    @commands.command()
    async def ranking(self,ctx):
        with open("data/data.json") as f:
            d = json.load(f)
        d = dict(sorted(d[str(ctx.guild.id)].items(),key=lambda x:x[1]["num"],reverse=True))
        l = []
        l2 = []
        l3 = []
        for i in d.keys():
            l2.append(d[i]["num"])
            l3.append(d[i]["count"])
            l.append(i)
        await ctx.channel.send(embed=discord.Embed(
          title="寄付ランキング",
          description="\n".join(["<@{}>\n寄付額:{}, 記録回数:{}".format(uid,num,count) for uid,num,count in zip(l,l2,l3)])
        ))
        
        

def setup(bot):
    return bot.add_cog(CCC(bot))