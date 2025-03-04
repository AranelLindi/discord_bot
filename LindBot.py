# Discord-Bibliotheken
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio  # Für das asynchrone Starten

# Token und Konfiguration laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents setzen
intents = discord.Intents.default()
intents.message_content = True

# Bot initialisieren
bot = commands.Bot(command_prefix="!", intents=intents)

# Fehlerbehandlung (muss VOR dem Bot-Start definiert werden!)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Fehlendes Argument. Nutze `!help [Befehl]` für Details.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unbekanntes Kommando. Nutze `!help`, um verfügbare Kommandos zu sehen.")
    else:
        print(f"Fehler: {error}")

# Event für Bot-Start
@bot.event
async def on_ready():
    print(f'\nBot eingeloggt als: {bot.user.name} - {bot.user.id}')
    print(f'Version: {discord.__version__}\n')

# Lade alle Cogs (Module)
async def load_extensions():
    for cog in ["general", "voting", "calendar"]:
        await bot.load_extension(f"cogs.{cog}")
    print("Alle Module erfolgreich geladen!")

# Hauptfunktion, die alles startet
async def main():
    await load_extensions()
    await bot.start(TOKEN)

# Bot starten
asyncio.run(main())
