# Discord-Bibliotheken
import discord
from discord.ext import commands
# from discord.ext.commands import Bot # bin verwundert, dass ich das hier nicht brauche?! Zeigt zumindest keine Fehler an
#from discord.voice_client import VoiceClient
#import asyncio

# Python-Bibliotheken
import datetime  # Für time-Kommando

# Instanz von Client. Verbindung zu Discord:
client = discord.Client()

# Kommando-Präfix festlegen (muss vor jedem Kommando eingegeben werden (z.B. !Hallo))
bot = commands.Bot(command_prefix="!")


# ##############################################
# Ein Event asynchron registrieren:
@bot.event
async def on_ready():  # on_ready wird aufgerufen, wenn der Bot sich eingeloggt hat
    #print("We have logged in successfully as {0.user}".format(client))
    print(
        f'\nWe have logged in successfully as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
# ##############################################


# Was macht das?

# @bot.command()
# async def clean(ctx, *, content: commands.clean_content(use_nicknames=False)):
#    await ctx.send(content)


# ############################################## DAS STAMMT NOCH AUS EINEM TUTORIAL! UNTERSUCHEN!
# Extra Klassen für darauf folgendes Command
# sofern möglich, die Klasse in extra Datei auslagern! (Das funktioniert über Cogs!)
class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @property
    def delta(self):
        return self.joined - self.created


class JoinDistanceConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return JoinDistance(member.joined_at, member.created)


@bot.command()
async def delta(ctx, *, member: JoinDistanceConverter):
    is_new = member.delta.days < 100
    if is_new:
        await ctx.send("Hey you're pretty new!")
    else:
        await ctx.send("Hm you're not so new.")


@bot.command()
async def joined(ctx, *, member: discord.member):
    await ctx.send('{0} joined on {0.joined_at}'.format(member))
# ##############################################


# @bot.command()
# async def leave(ctx):
#    await ctx.voice_client.disconnect()

# ##############################################
""" Anmerkung:
    Ein Kommando kann auf zwei äquivalente Arten definiert werden:

    @bot.command(...)
    async def ...

     -oder-
    
    @commands.command(...)
    async def ...

    bot.add_command(...)
"""
# ##############################################
#
#
# ############################################## (Nice to have ua als Testkommando, funktioniert immer)
# ---------Postet-die-aktuelle-Uhrzeit----------
# ##############################################


@bot.command(name='time')
async def time(ctx):
    print("We recognized a command!")
    current_time = datetime.datetime.strftime(
        datetime.datetime.now(), "%H:%M, %Y-%m-%d")
    await ctx.send(current_time)
# ##############################################
#
#
# ############################################## FUNKTIONIERT NOCH NICHT!
# ------------Joint-einem-Channel---------------
# ##############################################


@bot.command(name="join_channel", help="Makes the bot join a channel!", aliases=["join"])
async def join(ctx, arg):
    print("Joining channel " + arg)
    author = ctx.message.author
    channel = author.voice.voice_channel
    await channel.connect(reconnect=True)
# bot.add_command(join)
# ##############################################
#
#
# ##############################################
# ----------------ABSTIMMUNG--------------------
# ##############################################
#
ongoingVote = False  # globale Variable: Möchte eine Funktion diese verwenden,
# muss diese in der Funktion mit 'global CurrentVoting' erneut deklariert werden!
# Gibt an, ob aktuell eine Abstimmung läuft. Es kann immer nur eine aktiv sein!

# Startet eine Abstimmung und lädt das entsprechende Cog nach:


@bot.command(name='Voting')
async def voting(ctx, frage: str, *wahloptionen):
    global ongoingVote
    if ongoingVote == True:
        await ctx.send("Sorry, es läuft bereits eine Abstimmung!")
        return
    if len(frage) == 0:
        await ctx.send("Fehlendes Abstimmungsargument!")
        return

    # Vorprüfung: Anzahl der Wahlmöglichkeiten prüfen und erfassen:
    number = 1  # fortlaufende Nummer um Wahlmöglichkeiten durchzunummerieren
    zeichenkette = ""  # Alle Wahlmöglichkeiten verbinden und in einer Nachricht posten
    argumentList = []  # Nötig für Übergabe an VotingClass: Sammeln aller Wahloptionen als List()

    # durch Optionen iterieren:
    for option in wahloptionen:
        zeichenkette += "***" + str(number) + "***.) " + option + "\n"
        argumentList.append(option)
        number += 1

    # letzte Addition rückgängig machen, damit number gleichzeitig Anzahl Wahloptionen darstellt:
    number -= 1

    # Sicherheitsabfrage: Es müssen wenigstens zwei Abstimmungsoptionen zur Verfügung stehen, alles andere macht keinen Sinn:
    if number < 2:
        await ctx.send("Du musst mindestens zwei Wahlmöglichkeiten festlegen! Abbruch!")
        return

    # Läuft noch keine Abstimmung und stimmen sonst alle Bedingungen, die globale Variable auf True setzen und
    # mit dem weiteren Prozedere fortfahren:
    ongoingVote = True

    # Usern alles mitteilen: (vielleicht noch zum Ende verschieben, da dann Kommandos schon geladen sind und keine Verzögerung mehr entstehen könnte)
    await ctx.send(f"*Abstimmung von* __{ctx.author.name}__ *über folgendes Thema gestartet*: ***" + frage + "***")
    await ctx.send("__**Zur Auswahl stehen:**__\n" + zeichenkette + "\n\nMach mit und stimme ab mit: **!Vote Nr**")

    # Abstimmungsklasse laden: (d. h. Kommandos laden und verfügbar machen)
    bot.load_extension('VotingClass')

    # Klassenreferenz erhalten um Daten an VotingClass schicken zu können:
    staticVotingObject = bot.get_cog('VotingClass')
    print("Anzahl Argumente: " + str(number))
    # if vv is not None: # <------------------- braucht man das noch???????
    # Abstimmungsmöglichkeiten an die Klasse übergeben
    await staticVotingObject.addVotingOptions(number, argumentList)


# Beendet eine Abstimmung und entläd das entsprechende Cog (d.h. Kommandos die in VotingClass deklariert sind, funktionieren nicht mehr!)
@bot.command(name='CloseVoting')
async def CloseVoting(ctx):
    global ongoingVote  # globale Variable

    # Erste prüfen ob überhaupt eine Abstimmung gestartet wurde:
    if ongoingVote == True:
        bot.unload_extension('VotingClass')
        ongoingVote = False  # ermöglicht wieder eine Abstimmung
        await ctx.send("Abstimmung beendet!")
#
#
# ##############################################
# ---------------WOHER-KOMME-ICH?---------------
# ##############################################
#


@bot.command(name='Computer_wer_hat_Sie_erschaffen?')
async def creator(ctx):
    await ctx.send(f"Das, mein Lieber {ctx.author.name}," +
                   "war der allseits bekannte und beliebte Programmierer" +
                   "Stefan Lindörfer im Jahre des Herrn 2020!")
#
#
# ##############################################
# -----------MÜLLHAUFEN-(RECYCELBAR!)-----------
# ##############################################
# Event on_message wird für jede eingehende Nachricht gefeuert
# @bot.event
# async def on_message(message):
    # await message.channel.send(message.author.id)
    # if message.author == client.user: # soll verhindern, dass der Bot auf Messages von sich selbst reagiert
    #    return

    # Prüfen ob die Nachricht mit einem bestimmten Schlüsselwort beginnt:
    # if message.content.startswith('Hallo'):
    # await message.channel.send(f'Hallo {message.author.id}!')

#    if message.content.startswith('Tutorial'):
#        await message.channel.send("Hallo Welt!")

#    if message.content.startswith('oder LindBot?'):
#        await message.channel.send('Ja, du hast recht!')

# @client.event
# async def on_member_join():

# @bot.command(pass_context=True)
# async def join(ctx):
#    author = ctx.message.author
#    channel = author.voice_channel
#    await channel.connect()
    # await bot.join(channel)
#
#
# ##############################################
# -------------FEHLERABFANGROUTINE--------------
# ##############################################

# Fängt Fehler ab (evtl. noch spezifizieren und Fehlerbeschreibung direkt posten)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command...")


# ##############################################
# -------------------RUN IT---------------------
# ##############################################

# Discord Token darf nicht im Internet veröffentlicht werden. Daher:
# das Token in einem seperatem File speichern und diese in die .gitignore
# Datei aufnehmen, sodass keine Veröffentlichung stattfindet.

file_object = open(".token", "r")

token = file_object.read()

bot.run(token, bot=True, reconnect=True)  # "entweder/oder" ?
# client.run(token)
