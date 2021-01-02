from discord.ext import commands
from pymongo import MongoClient

import discord


class reactionroles(commands.Cog):
    """Make reaction roles for your server"""

    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.data = mcl.Elevate.rroles

    @commands.group(aliases=["reactionroles", "rroles"], invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def reactroles(self, ctx):
        """Manage reaction roles for your server"""
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @reactroles.command()
    async def add(
        self, ctx, channel: discord.TextChannel, msgid: int, role: discord.Role, emoji
    ):
        """Add a reaction/role pair"""
        try:
            msg = await channel.fetch_message(msgid)
            await msg.add_reaction(emoji)
            if isinstance(emoji, discord.Emoji):
                emoji = emoji.id
        except discord.NotFound:
            return await ctx.send("I couldn't find that message!")
        self.data.insert_one(
            {
                "chnlid": channel.id,
                "msgid": msgid,
                "role": role.id,
                "emoji": emoji,
                "guildid": ctx.guild.id,
            }
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            doc = self.data.find_one(
                {
                    "guildid": payload.guild_id,
                    "msgid": payload.message_id,
                    "chnlid": payload.channel_id,
                }
            )
            if payload.event_type == "REACTION_ADD":
                if str(payload.emoji) == doc.get(
                    "emoji"
                ) or payload.emoji.id == doc.get("emoji"):
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    role = guild.get_role(doc.get("role"))
                    await member.add_roles(role, reason="Reaction Roles")
            elif payload.event_type == "REACTION_REMOVE":
                doc = self.data.find_one(
                    {
                        "guildid": payload.guild_id,
                        "msgid": payload.message_id,
                        "chnlid": payload.channel_id,
                    }
                )
                if str(payload.emoji) == doc.get(
                    "emoji"
                ) or payload.emoji.id == doc.get("emoji"):
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(doc.get("role"))
                    member = guild.get_member(payload.user_id)
                    await member.remove_roles(role, reason="Reaction Roles")
        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(reactionroles(bot))
