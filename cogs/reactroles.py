from discord.ext import commands
from pymongo import MongoClient

import discord

class reactionroles(commands.Cog):
    """Make reaction roles for your server"""
    
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.data = mcl.Titanium.rroles

    @commands.group(aliases=['reactionroles', 'rroles'])
    @commands.has_permissions(manage_roles=True)
    async def reactroles(self, ctx):
        """Manage reaction roles for your server"""

    @reactroles.command()
    async def add(self, ctx, channel: discord.TextChannel, msgid: int, role: discord.Role, emoji):
        """Add a reaction/role pair"""
        try:
            msg = await channel.fetch_message(msgid)
            await msg.add_reaction(emoji)
            if isinstance(emoji, discord.Emoji):
                emoji = emoji.id
        except discord.NotFound:
            return await ctx.send("I couldn\'t find that message!")
        self.data.insert_one({"chnlid": channel.id, "msgid": msgid, "role": role.id, "emoji": emoji, "guildid": ctx.guild.id})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            print(payload.event_type)
            doc = self.data.find_one({"guildid": payload.guild_id, "msgid": payload.message_id, "chnlid": payload.channel_id})
            print(doc)
            if payload.event_type == "REACTION_ADD":
                if str(payload.emoji) == doc.get("emoji") or payload.emoji.id == doc.get("emoji"):
                    user = self.bot.get_user(payload.user_id)
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(doc.get("role"))
                    await user.add_roles(role, reason = "Reaction Roles")
            elif payload.event_type == "REACTION_REMOVE":
                doc = self.data.find_one({"guildid": payload.guild_id, "msgid": payload.message_id, "chnlid": payload.channel_id})
                if str(payload.emoji) == doc.get("emoji") or payload.emoji.id == doc.get("emoji"):
                    user = self.bot.get_user(payload.user_id)
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(doc.get("role"))
                    await user.remove_roles(role, reason = "Reaction Roles")
        except:
            return


def setup(bot):
    bot.add_cog(reactionroles(bot))