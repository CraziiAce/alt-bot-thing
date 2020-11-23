from discord.ext import commands
import discord

from datetime import datetime
from pymongo import MongoClient

class modlog(commands.Cog):
    """Control Titanium's modlog"""
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.data = mcl.Titanium.modlog

    @commands.has_permissions(kick_members=True)
    @commands.group()
    async def modlogset(self, ctx):
        """Change modlog settings"""
    
    @modlogset.command()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel Titanium will send modlog cases in"""
        doc = self.data.find_one({"_id":ctx.guild.id})
        print(str(doc))
        if not doc:
            if channel and not doc:
                self.data.insert_one({"_id": ctx.guild.id, "chnl": channel.id})
                await ctx.send(f"Successfully set the modlog channel to {channel.mention}")
                return
            elif not channel:
                await ctx.send("You didn't specify a channel!")
                return
        elif doc:
            if not channel and not doc.get('chnl'):
                await ctx.send("You didn't specify a channel!")
                return
            elif not channel and doc.get('chnl'):
                self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$unset": {"chnl": ""}})
                await ctx.send("Channel cleared")
                return
            else:
                self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$set": {"chnl": channel.id}})
                await ctx.send(f"Successfully set the modlog channel to {channel.mention}")
                return
        else:
            await ctx.send(f"Sorry, but I encountered an unexpected error. Please contact support with `{ctx.prefix}supportrequest`")

    @modlogset.command()
    async def toggle(self, ctx, toggle: bool):
        """Set whether to send modlogs Options are true/false"""
        doc = self.data.find_one({"_id":ctx.guild.id})
        if doc:
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"domodlog": toggle}})
            if toggle:
                await ctx.send("I will now send a message whenevery a mod action is performed (if the channel is configured)")
            elif not toggle:
                await ctx.send("I will no longer send a message when a mod actions is performed")
        elif not doc:
            self.data.insert_one({"_id": ctx.guild.id, "domodlog": toggle})


    async def send_case(self, ctx, case_type, reason, victim):
        """Internal func to send cases"""
        doc = self.data.find_one({"_id":ctx.guild.id})
        numcases = doc.get("numcases")
        if not doc.get("domodlog") or not doc.get("chnl"):
            return False
        elif case_type == "kick":
            embed = discord.Embed(title=f"Kick | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: {ctx.author}")
        elif case_type == "ban":
            embed = discord.Embed(title=f"Ban | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: {ctx.author}")
        if case_type == "mute":
            embed = discord.Embed(title=f"Mute | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: {ctx.author}")
        embed.set_author(name=victim, icon_url=victim.avatar_url)
        embed.set_footer(text=f"{datetime.strftime(datetime.now(), '%B %d, %Y at %I:%M %p')}")

