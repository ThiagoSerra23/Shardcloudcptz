import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv
from utils.database import init_db

# Setup Logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("discord").setLevel(logging.WARNING)

# Load Env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Fix for asyncio event loop error (Python 3.10+ / Windows)
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Bot Setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Init DB before starting
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    print("✅ Database initialized")
except Exception as e:
    print(f"❌ Failed to init database: {e}")

# Load Cogs
cogs_list = [
    "cogs.admin",
    "cogs.registration",
    "cogs.approval",
    "cogs.logs",
    "cogs.voice_control",
    "cogs.cast"
]

for cog in cogs_list:
    try:
        bot.load_extension(cog)
        print(f"✅ Loaded extension: {cog}")
    except Exception as e:
        print(f"❌ Failed to load extension {cog}: {e}")

@bot.event
async def on_ready():
    await init_db()
    print(f"🚀 Bot logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in .env file.")
    else:
        bot.run(TOKEN)
