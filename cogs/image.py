import discord

from discord.ext import commands
from PIL import Image as image # so I can name the cog Image while still using the PIL class
from PIL import ImageFile
from io import BytesIO
from typing import Union
import re


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url_regex = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        self.invis = 0x2F3136


    @staticmethod
    def filter_communist(img: Union(discord.Asset, str)):
        img = image.open(img)
        back = image.open("cogs/imgen/soviet.jpg")
        back = back.resize(img.size)
        blended_img = image.blend(img, back, 0.5)
        buffer = BytesIO()
        blended_img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @staticmethod
    def determine_command_subject(self, ctx, apply_command_to: typing.Union(discord.User, discord.Emoji, str) = None):
        if not apply_command_to:
            return ctx.author.avatar_url_as("jpg")
        elif isinstance(apply_command_to, discord.User):
            return apply_command_to.avatar_url_as("jpg")
        elif isinstance(apply_command_to, discord.Emoji):
            return apply_command_to.url_as("jpg")
        elif isinstance(apply_command_to, str):
            if re.match(self.url_regex, apply_command_to):
                return str(apply_command_to)
            else:
                return False

    @commands.command()
    async def communism(self, ctx, apply_filter_to = None):
        """Apply a communist filter to the specified member/emoji/image.\n
        If no member/emoji/image"""
        img = self.determine_command_subject(ctx, apply_filter_to)
        if not isinstance(img, str):
            img = BytesIO(await img.read())
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.filter_communist, img)
        else:
            img = BytesIO(img)
            img.seek(0)
            buffer = await self.bot.loop.run_in_executor(None, self.filter_communist, img)
        file=discord.File(buffer, filename="embossed.png")
        e=discord.Embed(color=self.invis)
        e.set_author(name="Embossed Avatar", icon_url=ctx.author.avatar_url)
        e.set_image(url="attachment://embossed.png")
        await ctx.remove(file=file, embed=e)

        
        


def setup(bot):
    bot.add_cog(Image(bot))