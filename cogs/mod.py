import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime
from asyncio import sleep
from typing import Union
from pymongo import MongoClient

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)

class mod(commands.Cog):
    '''Moderation Commands'''
    def __init__(self,bot):
        self.bot = bot
        self.no_resps = [
            'no',
            'No',
            'NO',
            'nO',
            'nope',
            'Nope',
        ]
        mcl = MongoClient()
        self.data = mcl.Titanium.modlog

    async def send_case(self, ctx, case_type, reason, victim):
        """Internal func to send cases"""
        doc = self.data.find_one({"_id": ctx.guild.id})
        if not doc.get("domodlog") or not doc.get("chnl"):
            return False

        if not doc.get("numcases"):
            numcases = 1
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"numcases": numcases}})
        elif doc.get("numcases"):
            numcases = doc.get("numcases") + 1
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"numcases": numcases}})

        if case_type == "kick":
            embed = discord.Embed(title=f"Kick | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: {ctx.author}")
        elif case_type == "ban":
            embed = discord.Embed(title=f"Ban | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: {ctx.author}")
        elif case_type == "mute":
            embed = discord.Embed(title=f"Mute | Case #{numcases}", description=f"**Reason:** {reason}\n**Moderator**: {ctx.author}")
        embed.set_author(name=victim, icon_url=victim.avatar_url)
        embed.set_footer(text=f"{datetime.strftime(datetime.now(), '%B %d, %Y at %I:%M %p')}")
        chnl = self.data.get_channel(doc.get("chnl"))
        await chnl.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        """Kick a user from this server"""
        if ctx.author == user:
            await ctx.send("You cannot kick yourself.")
        elif user.top_role >= ctx.author.top_role:
            await ctx.send("Due to Discord role hierarchy rules, I cannot complete that action.")
            return
        else:
            await user.kick(reason=reason)
            embed = discord.Embed(title=f'Member {user} has been kicked.', color=color)
            embed.add_field(name="Reason", value=reason)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await self.send_case(ctx, "kick", reason, user)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Union[discord.Member, discord.User], *, reason: str = None):
        """Bans a user from this server."""
        if ctx.author == user:
            await ctx.send("You cannot ban yourself.")
        elif user.top_role >= ctx.author.top_role:
            await ctx.send("Due to Discord role hierarchy rules, I cannot complete that action.")
            return
        else:
            # If user is not in the guild ban the user's object
            if isinstance(user, discord.User):
                user = discord.Object(user.id)

            await ctx.guild.ban(user, reason=reason)
            
            embed = discord.Embed(title=f'User {user} has been banned from this server.', color=color)
            embed.add_field(name="Reason", value=reason)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
        

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, reason: str = None):
        """Prevents a user from speaking"""
        permissions = discord.Permissions(1049600)
        if ctx.author == user:
            await ctx.send("You cannot mute yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
            if rolem is None:
                rolem = await ctx.guild.create_role(name="Muted", permissions=permissions, hoist=False, color=discord.Color.light_gray())
            elif rolem not in user.roles:
                await user.add_roles(rolem, reason=reason)
                embed = discord.Embed(title=f'User {user.name} has been successfully muted.', color=0x2F3136)
                embed.add_field(name="Shhh!", value=":zipper_mouth:")
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'User {user.mention} is already muted.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes a user."""
        rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
        if rolem in user.roles:
            embed = discord.Embed(title=f'User {user.name} has been manually unmuted.', color=0x2F3136)
            embed.add_field(name="Welcome back!", value=":open_mouth:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.remove_roles(rolem)

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        """Delete a certain number of messages from this channel (max 100)"""
        if count > 100:
            count = 100
        await ctx.message.channel.purge(limit=count+1, bulk=True)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        """Nuke (delete all messages) in the specified channel. (if no channel is specified, this channel will be nuked)"""
        if not channel:
            channel = ctx.channel
        embed = discord.Embed(
            color=color,
            title=f":boom: Channel ({ctx.channel.name}) has been nuked :boom:",
            description=f"Nuked by: {ctx.author.name}#{ctx.author.discriminator}"
        )
        embed.set_footer(text=f"{datetime.strftime(datetime.now(), '%B %d, %Y at %I:%M %p')}")
        embed.set_thumbnail(url="https://media.giphy.com/media/oe33xf3B50fsc/giphy.gif")
        await ctx.send(f"Are you sure you would like to nuke {channel.mention}? (y/n)")
        try:
            confirmation = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await ctx.send(f"Ok, I won't nuke {channel.mention}")
        if confirmation and confirmation.content.startswith("y"):
            pos = ctx.channel.position
            await ctx.channel.delete()
            channel = await ctx.channel.clone()
            await channel.edit(position=pos)
            await channel.send(embed=embed)
        else:
            await ctx.send(f"Ok, I won't nuke {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        """Change the slowmode in the current channel."""
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode is now {seconds} seconds.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self , ctx, user : discord.Member, *, reason: str):
        '''Warn a Member'''
        if user.top_role >= ctx.author.top_role:
            await ctx.send("You can only warn people below you in role hierarchy.")
            return
        else:
            guild = ctx.guild
            embed = discord.Embed(title=f"You have been warned by {ctx.author} in {guild}", color=color)
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"Reason:", value=f'{reason}')
            await user.send(embed=embed)
            await ctx.send(f"⚠️ Warned {user} for {reason}.")


def setup(bot):
    bot.add_cog(mod(bot))
