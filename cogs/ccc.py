import discord
from discord.ext import commands

import re
import json

from module import dbmanager as dbm

class CCC(commands.Cog):
    """仮想通貨機能"""
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def ccc(self,ctx,message_id):
        """チャンネルの履歴から集計します
        
        # 引数
        トリガーとするメッセージID
        
        # 使い方
        実行したチャンネルのメッセージ履歴からトリガーに指定したメッセージまで数字の含まれるメッセージを取得し、ユーザー別に取得回数と数値の合計を集計します。
        遡ることのできる上限は300件です。
        !のついたメッセージは無視されます。
        """

        if not ctx.author.guild_permissions.administrator:
            return
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
        """サーバー内の所持通貨ランキングを表示します"""
        
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
    
    @commands.command()
    async def set_count(self,ctx,member: discord.Member,money):
        """メンバーを指定し個別に値を設定します
        
        # 引数
        変更する項目(回数:count,所持額:num), 変更した後の値
        
        # 使い方
        一つ目の引数に指定した項目の値を二つ目引数に指定した値に設定します。
        """

        if not ctx.author.guild_permissions.administrator:
            return
        await ctx.send(member.id)
        

    @commands.command(aliases=["cc"])
    async def count_control(self,ctx,userid,target,num):
        """指定したメンバーの現在の値から足し引きします
        
        # 引数
        変更するユーザーのid,変更する項目(回数:count,所持額:num), 変更した後の値
        
        # 使い方
        一つ目の引数に指定した項目の値に二つ目の引数に指定した値を足します。負の値も使えます。
        """

        if not ctx.author.guild_permissions.administrator:
            return
        if target not in ["num","count"]:
            await ctx.send("不明な引数")
            return
        with open("data/data.json","r") as f:
            d = json.load(f)
        try:
            d[str(ctx.guild.id)][str(userid)][target] += int(num)
        except:
            await ctx.send("不明な引数")
            return
        with open("data/data.json","w") as f:
            json.dump(d,f,indent=4)
        await ctx.send("値を設定しました")
    
    @commands.command()
    async def show(self,ctx,userid):
        """指定したメンバーの通貨に関するデータを表示します
        
        # 引数
        表示するユーザーのid
        """

        try:
            with open("data/data.json","r") as f:
                d = json.load(f)
            info = d[str(ctx.guild.id)][userid]
            user = await self.bot.fetch_user(int(userid))
            await ctx.send(embed=discord.Embed(
                title=f"{user.name}の情報",
                description=f"記録回数:{info['count']}\n寄付額:{info['num']}"
                ))
        except:
            await ctx.send("不明な引数")
    
    @commands.command()
    async def clear(self,ctx):
        """実行したサーバーの集計したデータを削除します
        
        # 実行可能
        管理者権限のあるメンバー
        """
        if ctx.author.guild_permissions.administrator:
            with open("data/data.json","r") as f:
                d = json.load(f)
            d[str(ctx.guild.id)] = {}
            with open("data/data.json","w") as f:
                json.dump(d,f,indent=4)
            await ctx.send("処理を完了しました")
            return
        await ctx.send("管理者権限のあるメンバーだけが実行できます")

    @commands.command()
    @commands.is_owner()
    async def sql(self,ctx,*,sql):
        if await dbm.change(sql):
            await ctx.send("成功")
        else:
            await ctx.send("失敗")

def setup(bot):
    return bot.add_cog(CCC(bot))