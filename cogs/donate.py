from discord.ext import commands, tasks
from aiohttp_requests import requests
from pymongo import MongoClient
import discord, datetime, json

tools = "utils/tools.json"
with open(tools) as f:
    data = json.load(f)
color = int(data["COLORS"], 16)
footer = str(data["FOOTER"])

tokenFile = "utils/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data["DONATETOKEN"]


class donate(commands.Cog):
    """settings for donating to Elevate"""

    def __init__(self, bot):
        self.bot = bot
        self.token = ""
        mcl = MongoClient()
        self.payments = mcl.Elevate.payments
        self.checkended.start()
        self.counter = 0

    def cog_unload(self):
        self.checkended.cancel()

    @tasks.loop(seconds=300)
    async def checkended(self):
        re = await requests.get(
            "https://donatebot.io/api/v1/donations/718663089318527016/new",
            headers={"Authorization": self.token},
        )
        r = await re.json()
        try:
            g = self.bot.get_guild(718663089318527016)
            c = g.get_channel(788484736347144202)
            for item in r["donations"]:
                g = self.bot.get_guild(718663089318527016)
                mem = g.get_member(item["buyer_id"])
                role = g.get_role(item["role_id"])
                c = g.get_channel(788484736347144202)
                if self.counter == 1:
                    await c.send("started")
                    self.counter += 1
                await mem.add_roles(role, reason=f"Transaction id {item['txn_id']}")
                time = datetime.datetime.utcfromtimestamp(item["timestamp"])
                self.payments.insert_one(
                    {
                        "_id": item["txn_id"],
                        "status": item["status"],
                        "buyer": {"email": item["buyer_email"], "id": item["buyer_id"]},
                        "isSub": item["recurring"],
                        "price": {"price": item["price"], "currency": item["currency"]},
                        "time": time,
                    }
                )
                emb = discord.Embed(title="New donation!", color=color)
                emb.add_field(
                    name="Info",
                    value=f"Transaction ID: {item['txn_id']}\nUse `e!donate info {item['txn_id']} for more!",
                )
                await c.send(embed=emb)
                r = await requests.post(
                    f"https://donatebot.io/api/v1/donations/718663089318527016/{item['txn_id']}/mark",
                    headers={"Authorization": self.token},
                )
        except:
            await c.send("no donations :(")


def setup(bot):
    bot.add_cog(donate(bot))