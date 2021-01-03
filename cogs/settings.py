from discord.ext import commands
import discord
from pymongo import MongoClient
from typing import Union

off = "<:xon:792824364658720808><:coff:792824364483477514>"
on = "<:xoff:792824364545605683><:con:792824364558843956>"


class config(commands.Cog):
    """Settings for Elevate"""

    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        db = mcl.Elevate
        self.prfx = db.prefixes
        self.welcome = db.welcome

    @commands.group(aliases=["set"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """Change Elevate's settings"""
        if not ctx.invoked_subcommand:
            emb = discord.Embed(title="Settings for Elevate", color=ctx.bot.color)
            emb.add_field(name="Welcomer", value="WIP")
            await ctx.send_help(ctx.command)

    @settings.command()
    async def prefix(self, ctx, *, prefix: str = None):
        """Set Elevate's prefix. If no prefix is specified, the prefix will be reset to default."""
        doc = self.prfx.find_one({"_id": ctx.guild.id})
        if not doc:
            if prefix and not doc:
                self.prfx.insert_one({"_id": ctx.guild.id, "prfx": prefix})
                await ctx.send(f"Successfully set the server prefix to {prefix}")
                return
            elif not prefix:
                await ctx.send("You didn't specify a prefix!")
                return
        elif doc:
            if not prefix and not doc.get("prfx"):
                await ctx.send("You didn't specify a prefix!")
                return
            elif not prefix and doc.get("prfx"):
                self.prfx.update_one(
                    filter={"_id": ctx.guild.id}, update={"$unset": {"prfx": ""}}
                )
                await ctx.send("Prefix cleared")
                return
            else:
                self.prfx.update_one(
                    filter={"_id": ctx.guild.id}, update={"$set": {"prfx": prefix}}
                )
                await ctx.send(f"Successfully set the server prefix to {prefix}")
                return

    @commands.has_permissions(kick_members=True)
    @settings.group(invoke_without_command=True)
    async def welcome(self, ctx):
        """Welcome members to your server!"""
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @welcome.command()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel Elevate will welcome members in"""
        doc = self.welcome.find_one({"_id": ctx.guild.id})
        if not doc:
            if channel and not doc:
                self.welcome.insert_one({"_id": ctx.guild.id, "chnl": channel.id})
                await ctx.send(
                    f"Successfully set the welcome channel to {channel.mention}"
                )
                return
            elif not channel:
                await ctx.send("You didn't specify a channel!")
                return
        elif doc:
            if not channel and not doc.get("chnl"):
                await ctx.send("You didn't specify a channel!")
                return
            elif not channel and doc.get("chnl"):
                self.welcome.update_one(
                    filter={"_id": ctx.guild.id}, update={"$unset": {"chnl": ""}}
                )
                await ctx.send("Channel cleared")
                return
            else:
                self.welcome.update_one(
                    filter={"_id": ctx.guild.id}, update={"$set": {"chnl": channel.id}}
                )
                await ctx.send(
                    f"Successfully set the welcome channel to {channel.mention}"
                )
                return
        else:
            await ctx.send(
                f"Sorry, but I encountered an unexpected error. Please contact support with `{ctx.prefix}supportrequest`"
            )

    @welcome.command()
    async def joinmsg(self, ctx, *, msg: str = None):
        """Set the message sent upon guild join"""
        doc = self.welcome.find_one({"_id": ctx.guild.id})
        if doc:
            if not msg and doc.get("joinmsg"):
                self.welcome.update_one(
                    filter={"_id": ctx.guild.id}, update={"$unset": {"joinmsg": None}}
                )
                await ctx.send("Channel cleared")
            elif msg and doc.get("joinmsg"):
                self.welcome.update_one(
                    filter={"_id": ctx.guild.id}, update={"$set": {"joinmsg": msg}}
                )
                await ctx.send(f"Successfully set the join message to {msg}")
        elif msg and not doc:
            self.welcome.insert_one({"_id": ctx.guild.id, "joinmsg": msg})
            await ctx.send(f"Successfully set the join message to {msg}")
        elif not msg:
            await ctx.send("You didn't specify a channel!")
        else:
            self.welcome.update_one(
                filter={"_id": ctx.guild.id}, update={"$set": {"joinmsg": msg}}
            )
            await ctx.send(f"Successfully set the join message to {msg}")

    @welcome.command()
    async def dojoins(self, ctx, toggle: bool):
        """Toggle sending join messages. Options are true and false."""
        doc = self.welcome.find_one({"_id": ctx.guild.id})
        if doc:
            self.welcome.update_one(
                filter={"_id": ctx.guild.id}, update={"$set": {"dojoins": toggle}}
            )
            if toggle:
                await ctx.send(
                    "I will now send a message when someone joins this server (if the channel and message are configured"
                )
            elif not toggle:
                await ctx.send(
                    "I will no longer send a message when someone joins this server"
                )
        elif not doc:
            self.welcome.insert_one({"_id": ctx.guild.id, "dojoins": toggle})

    @welcome.command()
    async def leavemsg(self, ctx, *, msg: str = None):
        """Set the message sent upon guild join"""
        doc = self.welcome.find_one({"_id": ctx.guild.id})
        if not msg and doc.get("leavemsg"):
            self.welcome.update_one(
                filter={"_id": ctx.guild.id}, update={"$unset": {"leavemsg": None}}
            )
            await ctx.send("Channel cleared")
        elif msg and doc.get("leavemsg"):
            self.welcome.update_one(
                filter={"_id": ctx.guild.id}, update={"$set": {"leavemsg": msg}}
            )
            await ctx.send(f"Successfully set the leave message to {msg}")
        elif msg and not doc:
            self.welcome.insert_one({"_id": ctx.guild.id, "leavemsg": msg})
            await ctx.send(f"Successfully set the join message to {msg}")
        elif not msg:
            await ctx.send("You didn't specify a channel!")
        else:
            self.welcome.update_one(
                filter={"_id": ctx.guild.id}, update={"$set": {"leavemsg": msg}}
            )
            await ctx.send(f"Successfully set the join messgage to {msg}")

    @welcome.command()
    async def doleaves(self, ctx, toggle: bool):
        """Toggle sending join messages. Options are true and false."""
        doc = self.welcome.find_one({"_id": ctx.guild.id})
        if doc:
            self.welcome.update_one(
                filter={"_id": ctx.guild.id}, update={"$set": {"doleaves": toggle}}
            )
            if toggle:
                await ctx.send(
                    "I will now send a message when someone leaves this server (if the channel and message are configured)"
                )
            elif not toggle:
                await ctx.send(
                    "I will no longer send a message when someone leaves this server"
                )
        elif not doc:
            self.welcome.insert_one({"_id": ctx.guild.id, "doleaves": toggle})

    @welcome.command()
    async def dm(self, ctx, toggle: Union[bool, str]):
        """Set whether or not to dm users"""
        doc = self.welcome.find_one({"_id": ctx.guild.id})
        if doc:
            self.welcome.update_one(
                filter={"_id": ctx.guild.id}, update={"$set": {"dm": toggle}}
            )
            if toggle:
                await ctx.send(
                    "I will now send a DM when someone joins this server (if the channel and message are configured)"
                )
            elif not toggle:
                await ctx.send(
                    "I will no longer send a DM when someone joins this server"
                )
        elif not doc:
            self.welcome.insert_one({"_id": ctx.guild.id, "dm": toggle})


def setup(bot):
    bot.add_cog(config(bot))
