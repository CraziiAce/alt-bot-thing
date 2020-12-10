from discord.ext import commands
from pymongo import MongoClient
from typing import Union
from babel import lists
import discord, asyncio

class lockdown(commands.Cog):
    """Lock down your server."""
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.data = mcl.Elevate.lockdown

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def lockdownset(self, ctx):
        """Settings for the lockdown command"""
        pass

    @lockdownset.command()
    async def exclude(self, ctx, chnl: Union[str, discord.TextChannel]):
        """
        Exclude a channel from the lockdown. This is useful for channels that the `@everyone` role cannot see.
        Say `all` to exclude all channels.
        """
        if not chnl:
            return await ctx.send("You didn't specify a channel!")
        elif isinstance(chnl, str):
            if "all" in chnl.lower():
                async with ctx.typing():
                    ids = []
                    for channel in ctx.guild.channels:
                        ids.append(channel.id)
                    doc = self.data.find_one({"_id":ctx.guild.id})
                    if not doc:
                        self.data.insert_one({"_id": ctx.guild.id, "excluded": ids})
                        await ctx.send(f"Successfully excluded all channels")
                        return
                    elif doc:
                        self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$set": {"excluded": ids}})
                        await ctx.send(f"Successfully excluded all channels")
                        return
                    else:
                        await ctx.send(f"Sorry, but I encountered an unexpected error. Please contact support with `{ctx.prefix}supportrequest`")
            else:
                await ctx.send("That isn't a valid argument! Either put in a channel or `all`")
        elif isinstance(chnl, discord.TextChannel):
            async with ctx.typing():
                doc = self.data.find_one({"_id":ctx.guild.id})
                if not doc:
                    self.data.insert_one({"_id": ctx.guild.id, "excluded": [chnl.id]})
                    await ctx.send(f"Successfully excluded all channels")
                    return
                elif doc:
                    ids = doc.get("excluded")
                    if ids:
                        ids = ids.append(chnl.id)
                    else:
                        ids = [chnl.id]
                    self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$set": {"excluded": ids}})
                    await ctx.send(f"Successfully excluded all channels")
                    return
                else:
                    await ctx.send(f"Sorry, but I encountered an unexpected error. Please contact support with `{ctx.prefix}supportrequest`")
        else:
            await ctx.send("That isn't a valid argument! Either put in a channel or `all`")

    @lockdownset.command()
    async def include(self, ctx, chnl: Union[discord.TextChannel, str, int]):
        """
        Include a channel from the lockdown. This is useful if you excluded all channels.
        Say `all` to include all channels.
        """
        if not chnl:
            return await ctx.send("You didn't specify a channel!")
        elif isinstance(chnl, str):
            if "all" in chnl.lower():
                async with ctx.typing():
                    ids = []
                    for channel in ctx.guild.channels:
                        ids.append(channel.id)
                    doc = self.data.find_one({"_id":ctx.guild.id})
                    if not doc:
                        self.data.insert_one({"_id": ctx.guild.id, "included": ids})
                        await ctx.send(f"Successfully included all channels")
                        return
                    elif doc:
                        self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$set": {"included": ids}})
                        await ctx.send(f"Successfully included all channels")
                        return
                    else:
                        await ctx.send(f"Sorry, but I encountered an unexpected error. Please contact support with `{ctx.prefix}supportrequest`")
            else:
                await ctx.send("That isn't a valid argument! Either put in a channel or `all`")
        elif isinstance(chnl, discord.TextChannel):
            async with ctx.typing():
                doc = self.data.find_one({"_id":ctx.guild.id})
                if not doc:
                    self.data.insert_one({"_id": ctx.guild.id, "included": [chnl.id]})
                    await ctx.send(f"Successfully included all channels")
                    return
                elif doc:
                    ids = doc.get("included")
                    if ids:
                        ids = ids.append(chnl.id)
                    else:
                        ids = [chnl.id]
                    self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$set": {"included": ids}})
                    await ctx.send(f"Successfully included all channels")
                    return
                else:
                    await ctx.send(f"Sorry, but I encountered an unexpected error. Please contact support with `{ctx.prefix}supportrequest`")
        else:
            await ctx.send("That isn't a valid argument! Either put in a channel or `all`")
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        await ctx.send(f"Are you sure you would like to lockdown the server? (y/n)")
        try:
            confirmation = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await ctx.send(f"Ok, I won't lock down the server")
        if confirmation and confirmation.content.startswith("y"):
            everyone = ctx.guild.default_role
            async with ctx.typing():
                locked = []
                doc = self.data.find_one({"_id": ctx.guild.id})
                for chnl in ctx.guild.channels:
                    try:
                        if chnl.id in doc.get("excluded"):
                            pass
                        elif chnl.id in doc.get("included"):
                            await chnl.set_permissions(everyone, read_messages=True, send_messages=False, reason="Lockdown")
                            locked.append(str(chnl.mention))
                        if locked:
                            await ctx.send(f"Successfully locked down {lists.format_list(locked)}")
                    except TypeError:
                        continue


def setup(bot):
    bot.add_cog(lockdown(bot))