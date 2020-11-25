import discord, typing, logging, traceback

from aiohttp_requests import requests
from discord.ext import commands
from discord.ext.commands import Cog

from pymongo import MongoClient

log = logging.getLogger("protecc.errors")

# noinspection PyRedundantParentheses
class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.errmsgids=[]
        self.errathrids=[]
        mcl = MongoClient()
        self.data = mcl.Titanium.errors

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
        ignored_errors = (commands.CommandNotFound,)
        
        if isinstance(error, ignored_errors):
            return

        setattr(ctx, "original_author_id", getattr(ctx, "original_author_id", ctx.author.id))
        owner_reinvoke_errors = (
            commands.MissingAnyRole, commands.MissingPermissions,
            commands.MissingRole, commands.CommandOnCooldown, commands.DisabledCommand
        )

        if ctx.original_author_id in self.bot.owner_ids and isinstance(error, owner_reinvoke_errors):
            return await ctx.reinvoke()

        # Command is on Cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            return await self.send_to_ctx_or_author(ctx, f"This command is on cooldown. **Try in `{int(error.retry_after)}` seconds**", delete_after=10.0)

        # Missing argument
        elif isinstance(error, commands.MissingRequiredArgument):#{error.param.name}
            return await self.send_to_ctx_or_author(ctx, str(error))

        # Missing Permissions
        elif isinstance(error, commands.MissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f"You're missing the required permission: `{error.missing_perms[0]}`")

        # Missing Permissions
        elif isinstance(error, commands.BotMissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f"Titanium is missing the required permission: `{error.missing_perms[0]}`")

        # Discord Forbidden, usually if bot doesn't have permissions
        elif isinstance(error, discord.Forbidden):
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
                print(goodtb)
            logs = self.bot.get_channel(764576277512060928)
            doc = self.data.find_one({"id": "info"})
            if not doc:
                self.data.insert_one({"id": "info"})
            if not doc.get("numerror"):
                self.data.update_one(filter={"id": "info"}, update={"set": {"numerror": 0}})
            await ctx.send(f"```\nThis command raised an error: {error}.\nError ID: {ctx.message.id}.```")
            self.data.insert_one({"id": doc.numerror + 1, "command": ctx.command, "fulltb": f"https://hastebin.com/{re['key']}"})

            try:
                await logs.send(f"```xml\nAn error has been spotted in lego city! msg ID: {ctx.message.id}\nauthor name: {ctx.author.name}#{ctx.author.discriminator}\nauthor id: {ctx.author.id}\nguild: {ctx.guild.name}\nerror: {error}\ncommand: {ctx.message.content}```")
            except Exception as e:
                log.error(e)

    @commands.group()
    @commands.is_owner()
    async def error(self, ctx):
        """Resolve and manage errors"""

    @error.command()
    async def fix(self, ctx, errid: int):
        """Mark an error as fixed"""
        self.data.update_one(filter={"id": errid}, update={"$set": {"fixed": True}})
        await ctx.send(f"Successfully fixed error {errid}")

        
def setup(bot):
    bot.add_cog(ErrorHandler(bot))