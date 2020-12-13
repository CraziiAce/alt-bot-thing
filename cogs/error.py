import discord, typing, logging, traceback, json

from aiohttp_requests import requests
from discord.ext import commands
from discord.ext.commands import Cog
from datetime import datetime
from pymongo import MongoClient
from babel import lists

log = logging.getLogger("elevate.errors")

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)
footer = str(data['FOOTER'])



class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.errmsgids=[]
        self.errathrids=[]
        mcl = MongoClient()
        self.data = mcl.Elevate.errors
        self.color = color

    """Pretty much from here:
    https://github.com/4Kaylum/DiscordpyBotBase/blob/master/cogs/error_handler.py"""

    @commands.command()
    async def errortest(self, ctx):
        await ctx.send(reee)

    async def send_to_ctx_or_author(self, ctx, text: str = None, *args, **kwargs) -> typing.Optional[discord.Message]:
        """Tries to send the given text to ctx, but failing that, tries to send it to the author
        instead. If it fails that too, it just stays silent."""

        try:
            return await ctx.send(text, *args, **kwargs)
        except discord.Forbidden:
            try:
                return await ctx.author.send(text, *args, **kwargs)
            except discord.Forbidden:
                pass
        except discord.NotFound:
            pass
        return None


    @Cog.listener()
    async def on_command_error(self, ctx, error):        


        setattr(ctx, "original_author_id", getattr(ctx, "original_author_id", ctx.author.id))
        owner_reinvoke_errors = (
            commands.MissingAnyRole, commands.MissingPermissions,
            commands.MissingRole, commands.CommandOnCooldown, commands.DisabledCommand
        )

        if ctx.original_author_id in self.bot.owner_ids and isinstance(error, owner_reinvoke_errors):
            return await ctx.reinvoke()

        # Command is on Cooldown
        elif isinstance(error, commands.CommandNotFound):
            if ctx.invoked_subcommand:
                return
            else:
                get_help_for = ctx.message.content - len(ctx.prefix)
                
        elif isinstance(error, commands.CommandOnCooldown):
            return await self.send_to_ctx_or_author(ctx, f"This command is on cooldown. **Try in `{int(error.retry_after)}` seconds**", delete_after=10.0)

        # Missing argument
        elif isinstance(error, commands.MissingRequiredArgument):#{error.param.name}
            return await ctx.send_help(str(ctx.command))

        # Missing Permissions
        elif isinstance(error, commands.MissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f"You're missing the required permission: `{error.missing_perms[0]}`")

        # Missing Permissions
        elif isinstance(error, commands.BotMissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f"Titanium is missing the required permission: `{error.missing_perms[0]}`")

        # Discord Forbidden, usually if bot doesn't have permissions
        elif isinstance(error, discord.errors.Forbidden):
            return await self.send_to_ctx_or_author(ctx, f"I could not complete this command. This is most likely a permissions error.")

        # User who invoked command is not owner
        elif isinstance(error, commands.NotOwner):
            return await self.send_to_ctx_or_author(ctx, f"You must be the owner of the bot to run this command.")
        
        # Typehinted discord.Member arg not found
        elif isinstance(error, commands.MemberNotFound):
            return await self.send_to_ctx_or_author(ctx, f"I couldn't find the user {error.argument}")

        # same thing but user
        elif isinstance(error, commands.UserNotFound):
            return await self.send_to_ctx_or_author(ctx, f"I couldn't find the user {error.argument}")
        
        # ran guild command in DM
        elif isinstance(error, commands.NoPrivateMessage):
            return await self.send_to_ctx_or_author(ctx, "This command isn't available in DMs")

        else:
            etype = type(error)
            trace = error.__traceback__
            lines = traceback.format_exception(etype, error, trace)
            goodtb = ''.join(lines)
            try:
                r = await requests.post("https://hastebin.com/documents", data=goodtb)
                re = await r.json()
            except:
                log.error(goodtb)
            logs = self.bot.get_channel(778667649588527124)
            doc = self.data.find_one({"id": "info"})
            if not doc:
                self.data.insert_one({"id": "info"})
                doc = self.data.find_one({"id": "info"})
            if not doc.get("numerror"):
                self.data.update_one(filter={"id": "info"}, update={"$set": {"numerror": 0}})
            numerror = doc['numerror'] + 1
            emb = discord.Embed(title = f"An uncaught error occured!", description = f"I'm sorry, but an unexpected error occured. This has been sent to my development team for them to see. If you need help, feel free to join my [support server](https://discord.gg/zwyFZ7h)\n```\n{error}\n```")
            emb.set_footer(text = f"Caused by {str(ctx.command)} | ID: {numerror}")
            await ctx.send(embed=emb)
            self.data.insert_one({"id": numerror, "command": str(ctx.command), "fulltb": f"https://hastebin.com/{re['key']}", "datetime": datetime.now(), "fixed": False})
            self.data.update_one(filter={"id": "info"}, update={"$set": {"numerror": numerror, "fixed": True}})
            try:
                embed = discord.Embed(title=f"New error! ID: {numerror}", description=f"Erroring command: {str(ctx.command)}\nFull traceback: https://hastebin.com/{re['key']}", color=self.color)
                embed.set_footer(text=footer)
                await logs.send(embed=embed)
            except Exception as e:
                log.error(e)

    @commands.group()
    @commands.is_owner()
    async def error(self, ctx):
        """Resolve and manage errors"""
        pass

    @error.command()
    async def fix(self, ctx, errid):
        """Mark an error as fixed"""
        try:
            updt = self.data.update_one(filter={"id": int(errid)}, update={"$set": {"fixed": True}})
            await ctx.send(f"Successfully fixed error {errid}")
        except discord.errors.HTTPException:
            await ctx.send("HTTP exception")

    @error.command()
    async def info(self, ctx, id: int):
        """Get info for an error"""
        doc = self.data.find_one({"id": id})
        if not doc:
            await ctx.send("That error doesn't exist yet!")
        else:
            embed = discord.Embed(title=f"Info for error {id}", description=f"Erroring command: {doc['command']}\nFull traceback: {doc['fulltb']}", color=self.color)
            embed.set_footer(text=doc['datetime'].strftime("%b %d at %I:%M %p"))
            await ctx.send(embed=embed)


    @error.command()
    async def list(self, ctx):
        """List unsolved errors"""
        errors = []
        for error in self.data.find():
            if not error.get("fixed") and error.get("id") != 1 and error.get("id") != "info":
                errors.append(error['id'])
        try:
            embed = discord.Embed(title="Unsolved errors", description=lists.format_list(errors, locale="en"), color=self.color)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            await ctx.send("No unsolved errors exist! YAY!")
        
    @error.command()
    async def listbycmd(self, ctx):
        errors = {}
        for error in self.data.find():
            try:
                if not errors.get(error['command']):
                    errors[error['command']] = []
                    errors[error['command']].append(error['id'])
                elif errors.get(error['command']):
                    errors[error['command']].append(error['id'])
                else:
                    pass
            except:
                pass
        


def setup(bot):
    bot.add_cog(ErrorHandler(bot))