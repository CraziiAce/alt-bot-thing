import os
from utils.elevate import Elevate
import json
from discord.ext import commands

excluded = [
    "checks.py",
    "formats.py",
    "__init__.py",
    "paginator.py",
    "time.py",
    "del.py",
    "bancheck.py",
    "automod.py",
]

bot = Elevate()


os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename not in excluded:
        bot.load_extension(f"cogs.{filename[:-3]}")
        bot.log.info(f"Loaded cog {filename[:-3]}")


bot.load_extension("jishaku")

bot.run("OTM0NjkzNzc0MDg3NTU3MTMw.YezzaQ.MC5pJ9DGIhbgV3LNKY8n7f5dSvQ")
