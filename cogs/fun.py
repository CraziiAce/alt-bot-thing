import discord
from discord.ext import commands
import aiohttp
from aiohttp_requests import requests
from typing import Union

import random


class fun(commands.Cog):
    """Random Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession
        self.color = bot.color
        self.footer = bot.footer
        self.session = aiohttp.ClientSession()
        self.rps_choices = ["rock", "paper", "scissors"]

    async def rps_make_embed(self, choice: str, mychoice: str, iwon: Union[bool, str]):
        if not iwon:
            embed = discord.Embed(
                title="Rock Paper Scissors",
                description=f"I chose {mychoice} and you chose {choice}! {mychoice} beats {choice}, so I won!",
                color=self.color,
            )
        elif iwon is True:
            embed = discord.Embed(
                title="Rock Paper Scissors",
                description=f"I chose {mychoice} and you chose {choice}! {choice} beats {mychoice}, so you won!",
                color=self.color,
            )
        elif iwon == "tie":
            embed = discord.Embed(
                title="Rock Paper Scissors",
                description=f"I chose {mychoice} and you chose {choice}! No one won!",
                color=self.color,
            )
        return embed

    @commands.command()
    async def dice(self, ctx):
        """Roll a dice"""
        dice = ["1", "2", "3", "4", "5", "6"]
        embed = discord.Embed(
            title="Dice",
            description=f"The Dice Rolled {random.choice(dice)}",
            color=self.color,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png"
        )
        embed.set_footer(text=self.footer)
        await ctx.send(embed=embed)

        #    @commands.command()
        #    async def joke(self, ctx):
        #        """Get a joke"""
        #        async with self.session.get("https://dadjoke-api.herokuapp.com/api/v1/dadjoke") as r:
        #            resp = await r.json()
        #        await ctx.send(resp["joke"])

        @commands.command()
        async def binary(self, ctx, *, text: str):
            """Change text into binary"""
            if "@everyone" in text:
                await ctx.send("Please refrain from using `@everyone`.")
            elif "@here" in text:
                await ctx.send("Please refrain from using `@here`.")
            else:
                async with self.session.get(
                    f"https://some-random-api.ml/binary?text={text}"
                ) as resp:
                    resp = await resp.json()
                await ctx.send(resp["binary"])

        @commands.command()
        async def text(self, ctx, *, binary: str):
            """Change binary into text"""
            if (
                "010000000110010101110110011001010111001001111001011011110110111001100101"
                in binary
            ):
                await ctx.send("Please refrain from using `@everyone`.")
            elif "0100000001101000011001010111001001100101" in binary:
                await ctx.send("Please refrain from using `@here`.")
            else:
                async with self.session.get(
                    f"https://some-random-api.ml/binary?decode={binary}"
                ) as resp:
                    resp = await resp.json()
                await ctx.send(resp["text"])

    @commands.command()
    async def meme(self, ctx):
        """Get a random meme"""
        re = await requests.get("http://meme-api.herokuapp.com/gimme")
        r = await re.json()
        embed = discord.Embed(
            title=r["title"],
            url=r["postLink"],
            color=self.color,
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
            color=self.color,
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
            color=self.color,
        )
        embed.set_image(url=f"https://minotar.net/armor/body/{username}/100.png")
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{username}/100.png")
        embed.set_footer(text=self.footer)
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
            color=self.color,
        )
        embed.set_thumbnail(url=f"https://api.minetools.eu/favicon/{server}/25565")
        embed.set_footer(text=self.footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=["rps"])
    async def rockpaperscissors(self, ctx, choice: str):
        """
        Play rock paper scissors! `choice` should be either `rock`, `paper`, or `scissors`
        """
        choice = choice.lower()
        if choice not in self.rps_choices:
            return await ctx.send("That isn't a valid choice!")
        mychoice = random.choice(self.rps_choices)
        if choice == "rock":
            if mychoice == "rock":
                emb = await self.rps_make_embed(choice, mychoice, "tie")
            elif mychoice == "paper":
                emb = await self.rps_make_embed(choice, mychoice, False)
            elif mychoice == "scissors":
                emb = await self.rps_make_embed(choice, mychoice, True)
        elif choice == "paper":
            if mychoice == "paper":
                emb = await self.rps_make_embed(choice, mychoice, "tie")
            elif mychoice == "scissors":
                emb = await self.rps_make_embed(choice, mychoice, False)
            elif mychoice == "rock":
                emb = await self.rps_make_embed(choice, mychoice, True)
        elif choice == "scissors":
            if mychoice == "scissors":
                emb = await self.rps_make_embed(choice, mychoice, "tie")
            elif mychoice == "rock":
                emb = await self.rps_make_embed(choice, mychoice, False)
            elif mychoice == "paper":
                emb = await self.rps_make_embed(choice, mychoice, True)
        if isinstance(emb, discord.Embed):
            await ctx.send("is embed")
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(fun(bot))
