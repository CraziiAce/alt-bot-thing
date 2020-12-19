"""basically flare's cog"""

from discord.ext import commands
import discord, logging, json

log = logging.getLogger("Elevate.guild_join_manager")


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


class joinmessage(commands.Cog):
    """send a message upon guild join"""

    def __init__(self, bot):
        self.bot = bot
        self.color = bot.color
        self.footer = bot.footer

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = (
            discord.utils.find(lambda x: x.name in CHANNELS, guild.text_channels)
            or guild.system_channel
            or next(
                (
                    x
                    for x in guild.text_channels
                    if x.permissions_for(guild.me).send_messages
                ),
                None,
            )
        )
        emb = discord.Embed(
            title="Thanks for adding Elevate!",
            description="You can see all commands with e!help. If you ever have any questions, contact a support team member with `e!supportrequest`, or join the support server at discord.gg/zwyFZ7h",
            color=self.color,
        )

        emb.set_footer(text=self.footer)
        await channel.send(embed=emb)
        channel = self.bot.get_channel(733385692452880517)
        await channel.send(
            f"I just joined {guild} with {len(guild.members)} members! That's {len(self.bot.guilds)} servers now!"
        )


def setup(bot):
    bot.add_cog(joinmessage(bot))
