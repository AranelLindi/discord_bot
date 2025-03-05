import discord
from discord.ext import commands
import datetime
import random
import time
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # Bot instance (Discord structure)
        self.start_time = time.time() # Necessary to calculate uptime
        self.reminders = 0 # Counter for reminders

    async def cog_check(self, ctx):
        if not self.bot.active and ctx.command.name != "enable":
            return False
        return True
#    @commands.Cog.listener()
#    async def on_message(self, message):
#        if not self.active and not message.content.startswith("!"):
#            return # Ignores all messages if the bot is disabled
#        await self.bot.process_commands(message) # otherwise react to message according to commands

    @commands.command(name="time", help="Postet die aktuelle Uhrzeit")
    async def time(self, ctx):
        current_time = datetime.datetime.strftime(
            datetime.datetime.now(), "%H:%M, %Y-%m-%d %H:%M")
        await ctx.send(f"Die aktuelle Zeit ist: {current_time}")

    @commands.command(name="roll", help="Würfelt eine Zahl zwischen 1 und X (Standard: 6)")
    async def roll(self, ctx, max_number: int = 6):
        if max_number > 10e6:
            return

        result = random.randint(1, max_number)
        await ctx.send(f"{ctx.author.name} hat eine {result} gewürfelt!")

    @commands.command(name="flip", help="Wirft eine Münze")
    async def flip(self, ctx):
        result = random.choice(["Kopf", "Zahl"])
        await ctx.send(f"Die Münze zeigt: {result}!")

    @commands.command(name="ping", help="Zeigt die Latenz des Bots")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000) # in Millisekunden
        await ctx.send(f"Pong! Latenz: {latency}ms")

    @commands.command(name="uptime", help="Zeigt die Laufzeit des Bots")
    async def uptime(self, ctx):
        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"Der Bot läuft seit {hours}h {minutes}min {seconds}s.")

    @commands.command(name="remindme", help="Setzt eine Erinnerung")
    async def remindme(self, ctx, time_seconds: int, *, message: str):
        if self.reminders > 3:
            return

        self.reminders += 1

        try:
            await ctx.send(f"Erinnerung gesetzt für {time_seconds} Sekunden: {message}")
            await asyncio.sleep(time_seconds)
            await ctx.send(f"{ctx.author.mention}, Erinnerung: {message}")
        finally:
            self.reminders -= 1 # Finally guaranteers secure decrementation

    @commands.command(name='Computer_wer_hat_Sie_erschaffen?', help="")
    async def creator(self, ctx):
        await ctx.send(f"Das, mein Lieber {ctx.author.name}," +
                    "war der allseits bekannte und beliebte Programmierer" +
                    "Stefan Lindörfer im Jahre des Herrn 2020")
        
    @commands.command(name="disable", help="Deaktiviert den Bot (nur für Admins)")
    @commands.has_permissions(administrator=True) # Nur für Admins!
    async def disable(self, ctx):
        self.bot.active = False
        await ctx.send("LindBot wurde deaktiviert!")

    @commands.command(name="enable", help="Aktiviert den Bot wieder (Nur Admins)")
    @commands.has_permissions(administrator=True) # Nur für Admins
    async def enable(self, ctx):
        self.bot.active = True
        await ctx.send("LindBot wurde aktiviert")

    @commands.command(name="clear", help="Löscht die letzten X Nachrichten (nur Admins)")
    @commands.has_permissions(administrator=True) # Nur für Admins
    async def clear(self, ctx, amount: int = 0):
        if amount < 1:
            await ctx.send("Bitte gib eine Zahl größer als 0 an.")
            return
        
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"{len(deleted)} Nachrichten wurden gelöscht.", delete_after=5) # Antwort verschwindet nach 5 Sekunden

# Setup-Funktion, damit der Bot das Modul laden kann
async def setup(bot):
    await bot.add_cog(General(bot))
