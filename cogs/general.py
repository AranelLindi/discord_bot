import discord
from discord.ext import commands
import datetime
import random
import time
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(name="time", help="Postet die aktuelle Uhrzeit")
    async def time(self, ctx):
        current_time = datetime.datetime.strftime(
            datetime.datetime.now(), "%H:%M, %Y-%m-%d %H:%M")
        await ctx.send(f"Die aktuelle Zeit ist: {current_time}")

    @commands.command(name="roll", help="Würfelt eine Zahl zwischen 1 und X (Standard: 6)")
    async def roll(self, ctx, max_number: int = 6):
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
        await ctx.send(f"Erinnerung gesetzt für {time_seconds} Sekunden: {message}")
        await asyncio.sleep(time_seconds)
        await ctx.send(f"{ctx.author.mention}, Erinnerung: {message}")

    @commands.command(name='Computer_wer_hat_Sie_erschaffen?', help="")
    async def creator(self, ctx):
        await ctx.send(f"Das, mein Lieber {ctx.author.name}," +
                    "war der allseits bekannte und beliebte Programmierer" +
                    "Stefan Lindörfer im Jahre des Herrn 2020")

# Setup-Funktion, damit der Bot das Modul laden kann
async def setup(bot):
    await bot.add_cog(General(bot))
