import os, asyncio, discord, json, logging, datetime, aiohttp

from discord import Embed
from discord.ext import commands

from pymongo import MongoClient

log = logging.getLogger("elevate.core")
logging.basicConfig(
    level=logging.INFO,
    datefmt="%I:%M %p on %B %d %Y",
    format="%(asctime)s:%(levelname)s: %(name)s: %(message)s",
)


# support stuff
intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    allowed_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False),
)
bot.owner_ids = {555709231697756160}
# bot.remove_command("help")

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"


@bot.event
async def on_ready():
    log.info("{0.user} is up and running".format(bot))


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content.endswith("<@!763851389403136020>"):
        pass

@bot.command()
async def supportrequest(ctx, *, msg: str):
    """Send a message to my support team!"""
    emb = discord.Embed(
        title="Support Request!",
        description=f"Message: {msg}\nAuthor ID to reply: {ctx.author.id}",
    )
    time = datetime.datetime.now()
    time = time.strftime("%b %d at %I:%M %p")
    emb.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
    emb.set_footer(text=f"New support request by {ctx.author} on {time}")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(
            "https://canary.discord.com/api/webhooks/764934046940659762/sJOO0N6O2MHqRxpr1LyWRfPgBFzcyBFe1CnXV4gJ4OqmWWcx-Z49DZBAPceiixOZjDkA",
            adapter=discord.AsyncWebhookAdapter(session),
        )
        await webhook.send(
            embed=emb, username=ctx.author.name, avatar_url=ctx.author.avatar_url
        )
    await ctx.send("Message sent!")

@bot.command(aliases=["shutdown"])
@commands.is_owner()
async def restart(ctx):
    await ctx.send("👋 Bye!")
    await bot.logout()
    log.info("Protecc exited with exit code 0 (intentional)")

bot.load_extension("jishaku")