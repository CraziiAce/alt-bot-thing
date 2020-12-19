from discord.ext import commands

import dbl
import discord
import datetime
import json

tokenFile = "docker/utils/config.json"
with open(tokenFile) as f:
    data = json.load(f)
TOPTOKEN = data["TOPTOKEN"]


class TopGG(commands.Cog):
    """some bot owner utils"""

    def __init__(self, bot):
        self.token = TOPTOKEN
        self.color = bot.color
        self.footer = bot.footer
        self.bot = bot
        self.dblpy = dbl.DBLClient(
            self.bot,
            self.token,
            autopost=True,
            webhook_path="/dblwebhook",
            webhook_auth="elevate",
            webhook_port=6200,
        )

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(data)
        channel = self.bot.get_channel(733378752649625610)
        emb = discord.Embed(title="Vote recieved!", color=self.color)
        user = self.bot.get_user(int(data["user"]))
        emb.set_author(name=user, icon_url=user.avatar_url)
        time_bad = datetime.datetime.now()
        time_good = time_bad.strftime("%b %d at %I:%M %p")
        emb.set_footer(text=time_good)
        await channel.send(embed=emb)
        if not data["isWeekend"]:
            await user.send("Thanks for voting for me on top.gg!")
        if data["isWeekend"]:
            await user.send("Thanks for voting for me on top.gg!")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print(data)
        channel = self.bot.get_channel(733378752649625610)
        emb = discord.Embed(title="Test vote recieved!", color=self.color)
        user = self.bot.get_user(int(data["user"]))
        emb.set_author(name=user, icon_url=user.avatar_url)
        time_bad = datetime.datetime.now()
        time_good = time_bad.strftime("%b %d at %I:%M %p")
        emb.set_footer(text=time_good)
        await channel.send(embed=emb)


def setup(bot):
    bot.add_cog(TopGG(bot))
