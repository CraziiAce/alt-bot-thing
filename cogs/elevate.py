import discord, json, platform, sys, psutil, aiohttp, os, distro
from discord.ext import commands
from datetime import datetime
import subprocess as sp

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)

class Elevate(commands.Cog):
    '''Information about Elevate'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def vote(self, ctx):
        '''Vote for Elevate on top.gg'''
        embed=discord.Embed(title="Vote", description="**Vote for Elevate [here](https://top.gg/bot/716798638277525535/vote)", color=color)
        embed.set_footer(text="Elevate | discord.gg/zwyFZ7h")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def invite(self, ctx):
        '''Get the invite for the bot.'''
        emb = discord.Embed(
            title="Invite Elevate",
            description="Invite me [here](https://discord.com/oauth2/authorize?client_id=763851389403136020&permissions=268823638&scope=bot) with permissions, or [here](https://discord.com/oauth2/authorize?client_id=763851389403136020&permissions=0&scope=bot) without permissions"
        )
        emb.set_footer(text="Elevate | discord.gg/zwyFZ7h")
        await ctx.send(embed=emb)
        
    @commands.command()
    async def about(self, ctx):
        '''Get info about Elevate'''
        emb = discord.Embed(
            title="Elevate Info",
            description="A simple Discord bot with moderation tools and music",
            color=color
        )
        emb.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        emb.add_field(name= "News", value=f"**:wave: Elevate has a welcomer feature!** Use `{ctx.prefix}help welcomer`", inline=True)
        emb.add_field(name= ":link: Links", value="[Invite Elevate](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot)", inline=False)
        emb.set_footer(text="Elevate | discord.gg/zwyFZ7h")
        await ctx.send(embed=emb)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        supportembed = discord.Embed(title="Elevate support", color=color)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.add_field(name="Support Server", value="<a:igloading:737723292768796713> Support Server: https://discord.gg/zwyFZ7h", inline=False)
        supportembed.add_field(name="Contact", value="To contact support staff, use `t!support <message>`", inline=False)
        supportembed.set_footer(text=f"Use {ctx.prefix}help or info for more")
        await ctx.send(embed=supportembed)
    
    @commands.command()
    async def stats(self, ctx):
        """Get stats for Elevate"""
        dpy = discord.version_info
        d = distro.linux_distribution()
        ld = d[0] + " " + d[1]
        IS_LINUX = sys.platform == "linux"
        IS_WINDOWS = os.name == "nt"            
        embed = discord.Embed(title="Elevate Stats", color=color, description="Elevate | The only Discord bot you'll ever need\nDeveloped by CraziiAce#0001")
        embed.add_field(name="Python stats", value=f"Python version: **{platform.python_version()}**\ndiscord.py version: **{dpy.major}.{dpy.minor}.{dpy.micro}-{dpy.releaselevel}**\naiohttp version: **{aiohttp.__version__}**")
        embed.add_field(name="Bot stats", value=f"Servers: **{len(ctx.bot.guilds)}\n**Users: **{len(ctx.bot.users)}**\nEmojis: **{len(ctx.bot.emojis)}**\nCommands: **{len(ctx.bot.commands)}**", inline=False)
        if IS_LINUX:
            embed.add_field(name="Server stats", value=f"CPU current clockspeed: **{round(psutil.cpu_freq().current / 1000, 2)} GHz**\nCPU max clockspeed: **{round(psutil.cpu_freq().max / 1000, 2)} GHz**\nCPU usage: **{psutil.cpu_percent()}%\n**RAM:** {round(psutil.virtual_memory().total / 1000000)} MB\n**RAM usage:** {psutil.virtual_memory().percent}%**\nOperating system: **{platform.system()}**\nOS version: **{ld}**", inline=False)
        elif IS_WINDOWS:
            embed.add_field(name="Server stats", value=f"CPU current clockspeed: **{round(psutil.cpu_freq().current / 1000, 2)} GHz**\nCPU max clockspeed: **{round(psutil.cpu_freq().max / 1000, 2)} GHz**\nCPU usage: **{psutil.cpu_percent()}%\n**RAM:** {round(psutil.virtual_memory().total / 1000000)} MB\n**RAM usage:** {psutil.virtual_memory().percent}%**\nOperating system: **{platform.system()}**\nOS version: **{platform.platform()}**", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def privacy(self, ctx):
        """Get my privacy policy"""
        await ctx.send("Elevate takes your privacy very seriously. We only store data that is necessary to the operation of Elevate, like user IDs, guild IDs, role IDs, and channel IDs. Elevate accesses more extensive data on users, roles, guilds, and channels when certain commands are run, but it is not stored.\nThe data Elevate collects is stored only on the secure, password- and private-key protected servers that Elevate is run on, and except for some command arguments, is never sent anywhere.\n If you have any questions, DM CraziiAce#0001 on Discord")

    @commands.command()
    async def credits(self, ctx):
        """Get elevate's credits"""
        emb = discord.Embed(title = "Credits", description = "**Lead developer:** CraziiAce#0001\n**Help command & cog loader:** isirk#0001", color=color)
        await ctx.send(embed=embed)

     
def setup(bot):
    bot.add_cog(Elevate(bot))
