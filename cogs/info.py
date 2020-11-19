import discord

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo

import os

import json

import inspect

import random

import collections

import time, datetime
from datetime import datetime

from multiprocessing.connection import Client

from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)

class info(commands.Cog):
    '''Information Commands'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def vote(self, ctx):
        '''Vote for Titanum on top.gg'''
        embed=discord.Embed(title="Vote", description="**Vote for Titanium [here](https://top.gg/bot/751447995270168586/vote)**\nHave a cookie as well -> [🍪](https://orteil.dashnet.org/cookieclicker/)", color=color)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        await ctx.send('<https://discord.com/oauth2/authorize?client_id=763851389403136020&permissions=268823638&scope=bot>')
     
def setup(bot):
    bot.add_cog(info(bot))
