from discord.ext import commands
from typing import Union
import discord, random, json

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data["COLORS"], 16)
footer = str(data['FOOTER'])

class games(commands.Cog):
    """Play some games!"""
    def __init__(self, bot):
        self.bot = bot
        self.rps_choices = [
            "rock",
            "paper",
            "scissors"
        ]    
    async def make_embed(self, choice: str, mychoice: str, iwon: Union[bool, str]):
        if iwon == True:
            embed = discord.Embed(title="Rock Paper Scissors", description=f"I chose {mychoice} and you chose {choice}! {mychoice} beats {choice}, so I won!")
        elif iwon == False:
            embed = discord.Embed(title="Rock Paper Scissors", description=f"I chose {mychoice} and you chose {choice}! {choice} beats {mychoice}, so you won!")
        elif iwon == "tie":
            embed = discord.Embed(title="Rock Paper Scissors", description=f"I chose {mychoice} and you chose {choice}! No one one!")
        return embed

    @commands.command(aliases=['rps'])
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
                emb = self.make_embed(choice, mychoice, "tie")
            elif mychoice == "paper":
                emb = self.make_embed(choice, mychoice, False)
            elif mychoice == "scissors":
                emb = self.make_embed(choice, mychoice, True)
        elif choice == "paper":
            if mychoice == "paper":
                emb = self.make_embed(choice, mychoice, "tie")
            elif mychoice == "scissors":
                emb = self.make_embed(choice, mychoice, False)
            elif mychoice == "rock":
                emb = self.make_embed(choice, mychoice, True)
        elif choice == "scissors":
            if mychoice == "scissors":
                emb = self.make_embed(choice, mychoice, "tie")
            elif mychoice == "rock":
                emb = self.make_embed(choice, mychoice, False)
            elif mychoice == "paper":
                emb = self.make_embed(choice, mychoice, True)
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(games(bot))
            