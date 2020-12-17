from discord.ext import commands
import json
from statcord.client import Client

tokenFile = "utils/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data["STATCORD"]

class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = token
        self.api = Client(self.bot, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(StatcordPost(bot))
