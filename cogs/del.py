from discord.ext import commands, tasks
from aiohttp_requests import requests


class delpost(commands.Cog):
    """post discord extreme list stats"""

    def __init__(self, bot):
        self.bot = bot
        self.poster.start()

    @tasks.loop(minutes=10)
    async def poster(self):
        re = await requests.post(
            "https://api.discordextremelist.xyz/v2/bot/763851389403136020/stats"
        )
        if re.status == 200:
            print("ok")
