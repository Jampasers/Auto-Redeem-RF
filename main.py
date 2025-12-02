import os
import discord
from discord.ext import commands
from dotenv import load_dotenv 
from discord import app_commands
import sqlite3
load_dotenv()

# ==========================
# Intents
# ==========================
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

# ==========================
#  ERROR HANDLER
# ==========================
@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    # kalo command ada handler error sendiri (@cmd.error)
    if hasattr(ctx.command, "on_error"):
        return

    # Ambil error aslinya 
    error = getattr(error, "original", error)

    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have roles")
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.send("You don't have roles")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")
        return
    else:
        # Debug ke console + info singkat di Discord
        print(f"[COMMAND ERROR] {type(error).__name__}: {error}")
        await ctx.send("An error occured when running that command")

# ==========================
# SLASH COMMAND ERROR HANDLER
# ==========================
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole) or isinstance(error, app_commands.MissingAnyRole):
        msg = "You don't have roles"
    elif isinstance(error, app_commands.MissingPermissions):
        msg = "You don't have permissions"
    else:
        print(f"[SLASH ERROR] {type(error).__name__}: {error}")
        msg = "⚠️ Terjadi error saat menjalankan slash command ini.An error occured when running that command"

    # Interaction cuma boleh di-respond sekali, jadi perlu try/except
    try:
        await interaction.response.send_message(msg, ephemeral=True)
    except discord.InteractionResponded:
        await interaction.followup.send(msg, ephemeral=True)

async def load_cogs():
    """Memuat semua file .py di folder commands sebagai extension."""
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and filename != '__init__.py':
            # nama modul tanpa ekstensi
            await bot.load_extension(f'commands.{filename[:-3]}')

async def main():
    conn = sqlite3.connect("redeem.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS redeems (
        channel_id INTEGER PRIMARY KEY,
        user_id INTEGER
        email VARCHAR(64) NOT NULL,
        password VARCHAR(64) NOT NULL,
        balance INTEGER DEFAULT 0
    )            
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progres (
        user_id INTEGER PRIMARY KEY,
        redeem_code VARCHAR(12) NOT NULL,
        status TEXT CHECK(status IN ('sukses', 'pending', 'gagal'))
    )
    """)

    conn.commit()
    async with bot:
        await load_cogs()
        await bot.tree.sync()
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
