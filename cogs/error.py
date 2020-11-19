import discord
from discord.ext import commands
from discord.ext.commands import Cog

import typing

import logging
log = logging.getLogger("protecc.errors")

# noinspection PyRedundantParentheses
class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.errmsgids=[]
        self.errathrids=[]

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

        else:
            log.error(error)
            logs = self.bot.get_channel(764576277512060928)
            await ctx.send(f"```\nThis command raised an error: {error}.\nError ID: {ctx.message.id}.\nThis error has been sent to my owner, and I'll DM you if it's resolved. Thanks!\n```")
            self.errmsgids.append(ctx.message.id)
            self.errathrids.append(ctx.author.id)
            try:
                await logs.send(f"```\nAn error has been spotted in lego city! msg ID: {ctx.message.id}\nauthor name: {ctx.author.name}#{ctx.author.discriminator}\nauthor id: {ctx.author.id}\nguild: {ctx.guild.name}\nerror: {error}```")
            except:
                pass
    @commands.command()
    @commands.is_owner()
    async def resolveerror(self, ctx, errmsgid: int, msg: str = None):
        for id in self.errmsgids:
            if id == errmsgid:
                user = self.bot.get_user(self.errathrids[self.errmsgids.index(id)])
                await user.send(f"Hi!\nA command sent by you that returned an error message has been fixed.\nMy developers have asked me to send you this message: {msg}")
                await ctx.send(f"The message was succesfully sent to {user.name}#{user.discriminator}")
def setup(bot):
    bot.add_cog(ErrorHandler(bot))
