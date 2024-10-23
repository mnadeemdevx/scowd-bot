import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


initial_extensions = [
    "cogs.logging",
    "cogs.verification",
    "cogs.commands",
]


async def load_extensions():
    for extension in initial_extensions:
        await bot.load_extension(extension)


async def sync_commands():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Command sync failed: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await load_extensions()
    await sync_commands()


bot.run(os.getenv("TOKEN"))
