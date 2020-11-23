from discord.ext import commands
from pymongo import MongoClient

import discord

class welcomer(commands.Cog):
    """Welcome new members to your server"""
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        db = mcl.Titanium
        self.data = db.welcome
    
    @commands.has_permissions(kick_members = True)
    @commands.group()
    async def welcomeset(self, ctx):
        """Welcome members to your server!"""
        pass

    @welcomeset.command()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel Titanium will welcome members in"""
        doc = self.data.find_one({"_id":ctx.guild.id})
        print(str(doc))
        if not doc:
            if channel and not doc:
                self.data.insert_one({"_id": ctx.guild.id, "chnl": channel.id})
                await ctx.send(f"Successfully set the welcome channel to {channel.mention}")
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
                await ctx.send(f"Successfully set the welcome channel to {channel.mention}")
                return
        else:
            await ctx.send(f"Sorry, but I encountered an unexpected error. Please contact support with `{ctx.prefix}supportrequest`")

    @welcomeset.command()
    async def joinmsg(self, ctx, *, msg: str = None):
        """Set the message sent upon guild join"""
        doc = self.data.find_one({"_id":ctx.guild.id})
        if not msg and doc.get('joinmsg'):
            self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$unset": {"joinmsg": None}})
            await ctx.send("Channel cleared")
        elif msg and doc.get('joinmsg'):
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"joinmsg": msg}})
            await ctx.send(f"Successfully set the join message to {msg}")
        elif msg and not doc:
            self.data.insert_one({"_id": ctx.guild.id, "joinmsg": msg})
            await ctx.send(f"Successfully set the join message to {msg}")
        elif not msg:
            await ctx.send("You didn't specify a channel!")
        else:
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"joinmsg": msg}})
            await ctx.send(f"Successfully set the join message to {msg}")

    @welcomeset.command()
    async def dojoins(self, ctx, toggle: bool):
        """Toggle sending join messages. Options are true and false."""
        doc = self.data.find_one({"_id":ctx.guild.id})
        if doc:
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"dojoins": toggle}})
            if toggle:
                await ctx.send("I will now send a message when someone joins this server (if the channel and message are configured")
            elif not toggle:
                await ctx.send("I will no longer send a message when someone joins this server")
        elif not doc:
            self.data.insert_one({"_id": ctx.guild.id, "dojoins": toggle})

    @welcomeset.command()
    async def leavemsg(self, ctx, *, msg: str = None):
        """Set the message sent upon guild join"""
        doc = self.data.find_one({"_id":ctx.guild.id})
        if not msg and doc.get('leavemsg'):
            self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$unset": {"leavemsg": None}})
            await ctx.send("Channel cleared")
        elif msg and doc.get('leavemsg'):
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"leavemsg": msg}})
            await ctx.send(f"Successfully set the leave message to {msg}")
        elif msg and not doc:
            self.data.insert_one({"_id": ctx.guild.id, "leavemsg": msg})
            await ctx.send(f"Successfully set the join message to {msg}")
        elif not msg:
            await ctx.send("You didn't specify a channel!")
        else:
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"leavemsg": msg}})
            await ctx.send(f"Successfully set the join messgage to {msg}")
    
    @welcomeset.command()
    async def doleaves(self, ctx, toggle: bool):
        """Toggle sending join messages. Options are true and false."""
        doc = self.data.find_one({"_id":ctx.guild.id})
        if doc:
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"doleaves": toggle}})
            if toggle:
                await ctx.send("I will now send a message when someone leaves this server (if the channel and message are configured)")
            elif not toggle:
                await ctx.send("I will no longer send a message when someone leaves this server")
        elif not doc:
            self.data.insert_one({"_id": ctx.guild.id, "doleaves": toggle})

    @commands.Cog.listener()
    async def on_member_join(self, member):
        doc = self.data.find_one({"_id": member.guild.id})
        if doc['joinmsg'] and doc['chnl'] and doc['dojoins']:
            chnl = self.bot.get_channel(doc['chnl'])
            await chnl.send(doc['joinmsg'].format(user=member))
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        doc = self.data.find_one({"_id": member.guild.id})
        if doc['leavemsg'] and doc['chnl'] and doc['doleaves']:
            chnl = self.bot.get_channel(doc['chnl'])
            await chnl.send(doc['leavemsg'].format(user=member))

def setup(bot):
    bot.add_cog(welcomer(bot))