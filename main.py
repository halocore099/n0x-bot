import discord
from discord.ext import commands
import os
import asyncio
import json

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")   
            print(f"Loaded {filename}")

async def main():
    await load_extensions()
    await bot.start(config['token'])

asyncio.run(main())
    