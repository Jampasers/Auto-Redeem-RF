import os
import discord
from discord.ext import commands
from dotenv import load_dotenv 
load_dotenv()

# Intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(
    command_prefix='!',  
    intents=intents,
    case_insensitive=False
)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} berhasil login!')

async def load_cogs():
    """Memuat semua file .py di folder commands sebagai extension."""
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and filename != '__init__.py':
            # nama modul tanpa ekstensi
            await bot.load_extension(f'commands.{filename[:-3]}')

async def main():
    async with bot:
        await load_cogs()
        await bot.tree.sync()
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
