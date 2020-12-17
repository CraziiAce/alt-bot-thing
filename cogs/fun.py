import discord

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType
import aiohttp
import time, datetime
from datetime import datetime
from aiohttp_requests import requests

import os, io, json, asyncio, random, collections

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data["COLORS"], 16)
footer = str(data["FOOTER"])


class fun(commands.Cog):
    """Random Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession

    @commands.command()
    async def dice(self, ctx):
        """Roll a dice"""
        dice = ["1", "2", "3", "4", "5", "6"]
        embed = discord.Embed(
            title="Dice",
            description=f"The Dice Rolled {random.choice(dice)}",
            color=color,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png"
        )
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    #    @commands.command()
    #    async def joke(self, ctx):
    #        """Get a joke"""
    #        async with self.session.get("https://dadjoke-api.herokuapp.com/api/v1/dadjoke") as r:
    #            resp = await r.json()
    #        await ctx.send(resp["joke"])

    #    @commands.command()
    #    async def binary(self, ctx, *, text: str):
    #        """Change text into binary"""
    #        if "@everyone" in text:
    #            await ctx.send("Please refrain from using `@everyone`.")
    #        elif "@here" in text:
    #            await ctx.send("Please refrain from using `@here`.")
    #        else:
    #            async with self.session.get(f"https://some-random-api.ml/binary?text={text}") as resp:
    #                resp = await resp.json()
    #            await ctx.send(resp["binary"])

    #    @commands.command()
    #    async def text(self, ctx, *, binary: str):
    #        """Change binary into text"""
    #        if "010000000110010101110110011001010111001001111001011011110110111001100101" in binary:
    #            await ctx.send("Please refrain from using `@everyone`.")
    #        elif "0100000001101000011001010111001001100101" in binary:
    #            await ctx.send("Please refrain from using `@here`.")
    #        else:
    #            async with self.session.get(f"https://some-random-api.ml/binary?decode={binary}") as resp:
    #                resp = await resp.json()
    #            await ctx.send(resp["text"])

    @commands.command()
    async def meme(self, ctx):
        """Get a random meme"""
        re = await requests.get("http://meme-api.herokuapp.com/gimme")
        r = await re.json()
        embed = discord.Embed(
            title=r["title"],
            url=r["postLink"],
            color=color,
            description=f"u/{r['author']} | Can't see the image? [Click Here.]({r['url']})",
        )
        embed.set_footer(text=f"{r['ups']} 👍 | from r/{r['subreddit']}")
        embed.set_image(url=r["url"])
        await ctx.send(embed=embed)

    @commands.command(aliases=["ph"])
    async def programmerhumor(self, ctx):
        """Get a programmer humor meme"""
        re = await requests.get("http://meme-api.herokuapp.com/gimme/ProgrammerHumor")
        r = await re.json()
        embed = discord.Embed(
            title=r["title"],
            url=r["postLink"],
            color=color,
            description=f"u/{r['author']} | Can't see the image? [Click Here.]({r['url']})",
        )
        embed.set_footer(text=f"{r['ups']} 👍 | from r/{r['subreddit']}")
        embed.set_image(url=r["url"])
        await ctx.send(embed=embed)

    @commands.command(aliases=["mc"])
    async def minecraft(self, ctx, *, username):
        """Get a minecraft users stats"""
        async with self.session.get(
            f"https://api.mojang.com/users/profiles/minecraft/{username}?at="
        ) as resp:
            resp = await resp.json()
        embed = discord.Embed(
            title=f"Stats for {resp['name']}",
            description=f"ID: `{resp['id']}`",
            color=color,
        )
        embed.set_image(url=f"https://minotar.net/armor/body/{username}/100.png")
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{username}/100.png")
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=["mcs"])
    async def minecraftserver(self, ctx, *, server):
        """Get a minecraft servers stats"""
        async with self.session.get(
            f"http://mcapi.xdefcon.com/server/{server}/full/json"
        ) as resp:
            resp = await resp.json()
        embed = discord.Embed(
            title=f"Stats for {server}",
            description=f'IP: {resp["serverip"]}\nStatus: {resp["serverStatus"]}\nPing: {resp["ping"]}\nVersion: {resp["version"]}\nPlayers: {resp["players"]}\nMax Players: {resp["maxplayers"]}',
            color=color,
        )
        embed.set_thumbnail(url=f"https://api.minetools.eu/favicon/{server}/25565")
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(fun(bot))
