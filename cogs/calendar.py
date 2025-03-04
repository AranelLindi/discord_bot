import json
import os
import datetime
from discord.ext import commands

EVENTS_FILE = "events.json"

class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hilfsfunktion: Events laden
    def load_events(self):
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, "r") as f:
                return json.load(f)
        return {}
    
    # Hilfsfunktion: Events speichern
    def save_elements(self, events):
        with open(EVENTS_FILE, "w") as f:
            json.dump(events, f, indent=4)

    @commands.command(name="wochentag", help="Zeigt den Wochentag für ein bestimmtes Datum")
    async def wochentag(self, ctx, datum: str):
        try:
            date_obj = datetime.datetime.strptime(datum, "%d.%m.%Y").date()
            wochentag = date_obj.strftime("%A") # Gibt den Wochentag als String aus
            await ctx.send(f"Der {datum} fällt auf einen **{wochentag}**.")
        except ValueError:
            await ctx.send("Ungültiges Datum! Bitte nutze das Format DD.MM.YYYY.")

    @commands.command(name="addevent", help="Fügt ein Ereignis hinzu. Format: DD.MM.YYYY Name des Events")
    async def addevent(self, ctx, datum: str, *, name: str):
        try:
            event_date = datetime.datetime.strptime(datum, "%d.%m.%Y").date()
            today = datetime.date.today()

            if event_date <= today:
                await ctx.send("Ereignisse in der Vergangenheit können nicht hinzugefügt werden.")
                return
    
            events = self.load_events()
            events[datum] = name
            self.save_elements(events)
            await ctx.send(f"Ereignis **'{name}'** am **{datum}** gespeichert!")

        except ValueError:
            await ctx.send("Ungültiges Datum! Bitte nutze das Format DD.MM.YYYY.")
    
    @commands.command(name="listevents", help="Zeigt alle gespeicherten Ereignisse an")
    async def listevents(self, ctx):
        events = self.load_events()
        today = datetime.date.today()

        # Automatische Lösung aller Ereignisse
        events = {d: n for d, n in events.items() if datetime.datetime.strptime(d, "%d.%m.%Y").date() > today}
        self.save_elements(events)

        if events:
            message = "** Kommende Ereignisse:**\n"
            for datum, name in sorted(events.items()):
                message += f"{datum}: {name}\n"
        else:
            message = "Keine geplanten Ereignisse."

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Calendar(bot))