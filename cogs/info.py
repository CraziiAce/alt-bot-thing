import discord
from discord.ext import commands

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
        embed=discord.Embed(title="Vote", description="**Vote for Titanium [here](https://top.gg/bot/716798638277525535/vote)", color=color)
        embed.set_footer(text="Titanium | discord.gg/zwyFZ7h")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def invite(self, ctx):
        '''Get the invite for the bot.'''
        emb = discord.Embed(
            title="Invite Titanium",
            description="Invite me [here](https://discord.com/oauth2/authorize?client_id=763851389403136020&permissions=268823638&scope=bot) with permissions, or [here](https://discord.com/oauth2/authorize?client_id=763851389403136020&permissions=0&scope=bot) without permissions"
        )
        emb.set_footer(text="Titanium | discord.gg/zwyFZ7h")
        await ctx.send(embed=emb)
        
    @commands.command()
    async def about(self, ctx):
        '''Get info about Titanium'''
        emb = discord.Embed(
            title="Titanium Info",
            description="A simple Discord bot with moderation tools and music",
            color=color
        )
        emb.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        emb.add_field(name= "<:news:758781954073821194> News", value=f"**🎧 <@751447995270168586> Has music commands! 🎧**\n> To see the music commands use `{ctx.prefix}help music`!", inline=True)
        emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/758451109919981580.png?v=1")
        emb.add_field(name= ":link: Links", value="[Invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot)", inline=False)
        emb.set_footer(text="Titanium | discord.gg/zwyFZ7h")
        await ctx.send(embed=emb)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        supportembed = discord.Embed(title="Titanium support", color=color)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
        supportembed.add_field(name="Support Server", value="<a:igloading:737723292768796713> Support Server: https://discord.gg/zwyFZ7h", inline=False)
        supportembed.add_field(name="Contact", value="To contact support staff, use `t!support <message>`", inline=False)
        supportembed.set_footer(text=f"Use {ctx.prefix}help or info for more")
        await ctx.send(embed=supportembed)
     
def setup(bot):
    bot.add_cog(info(bot))
