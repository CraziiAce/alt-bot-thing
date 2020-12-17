from discord.ext import commands
from pymongo import MongoClient


class autorole(commands.Cog):
    """Automatically give users a role when the join the server"""

    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.data = mcl.Elevate.autorole

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx):
        """Automatically give a role to people who join the server"""
        pass


def setup(bot):
    bot.add_cog(autorole(bot))
