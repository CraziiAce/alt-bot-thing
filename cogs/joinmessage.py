"""basically flare's cog"""

from discord.ext import commands
import discord, logging

log = logging.getLogger("Starry.guild_join_manager")

CHANNELS = [
    "general",
    "general-chat",
    "основной",
    "основной-чат",
    "generell",
    "generell-chatt",
    "כללי",
    "צ'אט-כללי",
    "allgemein",
    "generale",
    "général",
    "općenito",
    "bendra",
    "általános",
    "algemeen",
    "generelt",
    "geral",
    "informații generale",
    "ogólny",
    "yleinen",
    "allmänt",
    "allmän-chat",
    "chung",
    "genel",
    "obecné",
    "obično",
    "Генерален чат",
    "общи",
    "загальний",
    "ทั่วไป",
    "常规",
]

MSG = discord.Embed(
    title="Thanks for adding Starry!",
    description="You can see all commands with t!help. If you ever have any questions, contact a support team member with `t.supportrequest`, or join the support server at discord.gg/zwyFZ7h"
)

class joinmessage(commands.Cog):
    """send a message upon guild join"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = (
            discord.utils.find(lambda x: x.name in CHANNELS, guild.text_channels)
            or guild.system_channel
            or next(
                (x for x in guild.text_channels if x.permissions_for(guild.me).send_messages), None
            )
        )

        await channel.send(embed=MSG)
        log.info("Guild welcome message sent in {}".format(guild))

def setup(bot):
    bot.add_cog(joinmessage(bot))