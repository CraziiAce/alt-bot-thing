from discord.ext import commands
import discord
from PyMongo import MongoClient


class config(commands.Cog):
    """Settings for Titanium"""
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        db = mcl.Titanium
        self.prfx = db.prefixes

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """Change Titanium's settings"""
        pass

    @settings.command()
    async def prefix(self, ctx, *, prefix: str = None):
        """Set Titanium's prefix. If no prefix is specified, the prefix will be reset to default."""
        doc = self.prfx.find_one({"_id":ctx.guild.id})
        if not doc:
            if prefix and not doc:
                self.prfx.insert_one({"_id": ctx.guild.id, "prfx": prefix})
                await ctx.send(f"Successfully set the server prefix to {prefix}")
                return
            elif not prefix:
                await ctx.send("You didn't specify a prefix!")
                return
        elif doc:
            if not prefix and not doc.get('self.prfx'):
                await ctx.send("You didn't specify a prefix!")
                return
            elif not prefix and doc.get('self.prfx'):
                self.prfx.update_one(filter = {"_id": ctx.guild.id}, update={"$unset": {"self.prfx": ""}})
                await ctx.send("Prefix cleared")
                return
            else:
                self.prfx.update_one(filter = {"_id": ctx.guild.id}, update={"$set": {"self.prfx": prefix}})
                await ctx.send(f"Successfully set the server prefix to {prefix}")
                return


