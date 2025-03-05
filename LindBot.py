# Discord-Bibliotheken
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio  # Für das asynchrone Starten
import sys

sys.stdout.reconfigure(line_buffering=True)

# Token und Konfiguration laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents setzen
intents = discord.Intents.default()
intents.message_content = True

# Bot initialisieren
bot = commands.Bot(command_prefix="!", intents=intents)
bot.active = True

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
    cogs = ["general", "voting", "calendar"] # Add further cogs here ...
    
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"Modul '{cog}' erfolgreich geladen.")
        except Exception as e:
            print(f"Fehler beim Laden von '{cog}': {e}")

# Hauptfunktion, die alles startet
async def main():
    await load_extensions()
    await bot.start(TOKEN)

# Nur starten, wenn die Datei direkt ausgeführt wird
if __name__ == '__main__':
    # Bot starten
    asyncio.run(main())
