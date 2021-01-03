from discord.ext import commands
from pymongo import MongoClient


class welcomer(commands.Cog):
    """Welcome new members to your server"""

    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        db = mcl.Elevate
        self.data = db.welcome

    @commands.Cog.listener()
    async def on_member_join(self, member):
        doc = self.data.find_one({"_id": member.guild.id})
        if doc.get("joinmsg") and doc.get("chnl") and doc.get("dojoins"):
            if not doc.get("dm"):
                chnl = self.bot.get_channel(doc["chnl"])
                await chnl.send(doc["joinmsg"].format(user=member))
            elif doc.get("dm"):
                await member.send(doc["joinmsg"].format(user=member))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        doc = self.data.find_one({"_id": member.guild.id})
        if doc.get("leavemsg") and doc.get("chnl") and doc.get("doleaves"):
            chnl = self.bot.get_channel(doc.get("chnl"))
            await chnl.send(doc.get("leavemsg").format(user=member))


def setup(bot):
    bot.add_cog(welcomer(bot))
