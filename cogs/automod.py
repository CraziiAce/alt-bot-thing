from discord.ext import commands
import discord
import re
from pymongo import MongoClient
from datetime import datetime

class Automod(commands.Cog):
    """Automod stuff"""
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.data = mcl.Starry.automod
        self.modlog = mcl.Starry.modlog
        self.accepted_actions = [
            "kick",
            "ban",
            "mute"
        ]
        self.yes_actions = [
            "yes",
            "Yes",
            "true",
            "True"
        ]
        self.no_actions = [
            "no",
            "No",
            "false",
            "False"
        ]
        self.regexes = {
            "link": "^https?:\/\/.*[\r\n]*"
        }
        self.offenses = [
            "link"
        ]

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def automod(self, ctx):
        """Automod settings"""
        pass

    @automod.command()
    async def antilink(self, ctx, do_antilink, action = None):
        """Toggle whether starry will do antilink. do_antilink should be true/false, and action should be either `kick`, `ban`, or `mute`."""
        if action not in self.accepted_actions:
            await ctx.send("That's not a valid action!")
        if do_antilink in self.no_actions:
            do_antilink = False
        if do_antilink in self.yes_actions:
            do_antilink = True
        doc = self.data.find_one({"guildid": ctx.guild.id, "offense": "link"})
        if not doc:
            self.data.insert_one({"guildid": ctx.guild.id, "offense": "link", "do": do_antilink, "action": action})
            if do_antilink:
                await ctx.send(f"Ok, I will now {action} someone if they post a link")
            if not do_antilink:
                await ctx.send("Ok, I won't do anything if someone posts a link")
            elif do_antilink not in self.no_actions and do_antilink not in self.yes_actions:
                return await ctx.send("Sorry, that isn\'t a valid action")
        elif doc:
            self.data.update_one(query = {"guildid": ctx.guild.id, "offense": link}, update = {"$set": {do: do_antilink, "action": action}})

    async def send_case(self, ctx, case_type, reason, victim):
        """Internal func to send cases"""
        doc = self.data.find_one({"_id": ctx.guild.id})
        if not doc.get("domodlog") or not doc.get("chnl"):
            return False

        if not doc.get("numcases"):
            numcases = 1
            self.modlog.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"numcases": numcases}})
        elif doc.get("numcases"):
            numcases = doc.get("numcases") + 1
            self.modlog.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"numcases": numcases}})

        if case_type == "kick":
            embed = discord.Embed(title=f"Kick | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: Automod")
        elif case_type == "ban":
            embed = discord.Embed(title=f"Ban | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: Automod")
        elif case_type == "mute":
            embed = discord.Embed(title=f"Mute | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: Automod")
        embed.set_author(name=victim, icon_url=victim.avatar_url)
        embed.set_footer(text=f"{datetime.strftime(datetime.now(), '%B %d, %Y at %I:%M %p')}")
        chnlid = int(doc.get("chnl"))
        chnl = self.bot.get_channel(chnlid)
        await chnl.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        for offense in self.offenses:
            doc = self.data.find_one({"guildid": message.guild.id, "offense": offense})
            if doc.get("do"):
                try:
                    if re.match(self.regexes[offense], message.content):
                        guild = self.bot.get_guild(message.guild.id)
                        member = guild.get_member(message.author.id)
                        if doc.get("action") == "ban":
                            emb = discord.Embed(title = f"Ban from {str(message.guild)}", description = "You were banned by my auto moderation feature.")
                            await member.send(embed=emb)
                            await guild.ban(member)
                        await self.send_case(message, doc.get("action"), offense, message.author)
                except Exception as e:
                    print(e)

def setup(bot):
    bot.add_cog(Automod(bot))   