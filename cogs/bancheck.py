from discord.ext import commands
from aiohttp_requests import requests
from pymongo import MongoClient
import discord, json, ksoftapi

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data["COLORS"], 16)
footer = str(data["FOOTER"])


tokenFile = "utils/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data["KSOFT"]


class bancheck(commands.Cog):
    """
    Use a lot of APIs and Elevate's own database to identify users that have been banned in other servers or have spammed/sent ads repeatedly.
    This feature is incomplete, so it may not work.
    Please report any bugs with `e!supportrequest`.
    """

    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.bans = mcl.Elevate.bans
        self.data = mcl.Elevate.bancheck
        self.kcl = ksoftapi.Client(token)

    @commands.group(invoked_without_command=True)
    @commands.has_permissions(manage_server=True)
    async def bancheckset(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @bancheckset.command()
    async def channel(self, ctx, chnl: discord.TextChannel = None):
        """
        Set the channel to send user's trust factors on join. Not specifying a channel will clear the channel, if it has already been set
        """
        doc = self.data.find_one({"_id": ctx.guild.id})
        if not doc:
            if chnl and not doc:
                self.data.insert_one({"_id": ctx.guild.id, "chnl": chnl.id})
                await ctx.send(
                    f"Successfully set the bancheck channel to {chnl.mention}"
                )
                return
            elif not chnl:
                await ctx.send("You didn't specify a channel!")
                return
        elif doc:
            if not chnl and not doc.get("chnl"):
                await ctx.send("You didn't specify a channel!")
                return
            elif not chnl and doc.get("chnl"):
                self.data.update_one(
                    filter={"_id": ctx.guild.id}, update={"$unset": {"chnl": ""}}
                )
                await ctx.send("Channel cleared")
                return
            else:
                self.data.update_one(
                    filter={"_id": ctx.guild.id}, update={"$set": {"chnl": chnl.id}}
                )
                await ctx.send(
                    f"Successfully set the bancheck channel to {chnl.mention}"
                )
                return

    @bancheckset.command()
    async def action(self, ctx, action: str):
        "" f"Set the action to take if a user has less than the trust level set with `{ctx.prefix}bancheckset trustlevel`.\nOptions are `kick`, `ban`, or `none` to clear" ""
        doc = self.data.find_one({"_id": ctx.guild.id})
        if not doc:
            self.data.insert_one({"_id": ctx.guild.id, "chnl": action})
            await ctx.send(f"Successfully set the bancheck action to {action}")
            return
        elif doc:
            self.data.update_one(
                filter={"_id": ctx.guild.id}, update={"$set": {"chnl": action}}
            )
            await ctx.send(f"Successfully set the bancheck action to {action}")
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        doc = self.data.find_one({"_id": member.guild.id})
        if not doc:
            return

    @commands.command()
    async def check(self, ctx, user: discord.User):
        """
        Check someones trust factor
        """
        re = requests.get(f"https://altdentifier.com/api/v2/user/{user.id}/trustfactor")
        if re.status == 200:
            return


def setup(bot):
    bot.add_cog(bancheck(bot))
