# Discord-Bibliotheken
import discord
from discord.ext import commands

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
    print(
        f'\nWe have logged in successfully as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
# ##############################################
#
#
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


# ############################################## (Nice to have ua als Testkommando, funktioniert immer)
# ---------Postet-die-aktuelle-Uhrzeit----------
# ##############################################
#
#
@bot.command(name='time', help="Postet aktuelle Zeit")
async def time(ctx):
    print("We recognized a command!")
    current_time = datetime.datetime.strftime(
        datetime.datetime.now(), "%H:%M, %Y-%m-%d")
    await ctx.send(current_time)
# ##############################################


# ##############################################
# ------------Joint-einem-Channel--------------- (FUNKTIONIERT NOCH NICHT!)
# ##############################################
#
#
# @bot.command(name="join_channel", help="Makes the bot join a channel!", aliases=["join"])
# async def join(ctx, arg):
#    print("Joining channel " + arg)
#    author = ctx.message.author
#    channel = author.voice.voice_channel
#    await channel.connect(reconnect=True)
# bot.add_command(join)
# ##############################################
#
#
# ##############################################
# ----------------ABSTIMMUNG--------------------
# ##############################################
#
# globale Variable: Gibt an, ob aktuell eine Abstimmung läuft. Es kann immer nur eine Abstimmung aktiv sein!
ongoingVote = False
# Möchte eine Funktion diese verwenden, muss diese in der Funktion mit 'global CurrentVoting' erneut deklariert werden!


# Startet eine Abstimmung und lädt das entsprechende Cog nach:
@bot.command(name='Voting')
async def voting(ctx, frage: str, *wahloptionen):  # * = variadic function argument!
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

    # letzte Addition rückgängig machen, damit number gleichzeitig [Anzahl Wahloptionen] darstellt:
    number -= 1

    # Sicherheitsabfrage: Es müssen wenigstens zwei Abstimmungsoptionen zur Verfügung stehen, alles andere macht keinen Sinn:
    if number < 2:
        await ctx.send("Abstimmung fehlgeschlagen, Du musst mindestens zwei Wahlmöglichkeiten festlegen!")
        return

    # Läuft noch keine Abstimmung und stimmen sonst alle Bedingungen, die globale Variable auf True setzen und mit dem weiteren Prozedere fortfahren:
    ongoingVote = True

    # Usern alles mitteilen: (vielleicht noch zum Ende verschieben, da dann Kommandos schon geladen sind und keine Verzögerung mehr entstehen könnte)
    await ctx.send(f"*Abstimmung von* __{ctx.author.name}__ *über folgendes Thema gestartet*: ***" + frage + "***")
    await ctx.send("__**Zur Auswahl stehen:**__\n" + zeichenkette + "\n\nMach mit und stimme ab mit: *!Vote [Nr]*")

    # Abstimmungsklasse laden: (d. h. Kommandos laden und verfügbar machen)
    bot.load_extension('VotingClass')

    # Klassenreferenz erhalten um Daten an VotingClass schicken zu können:
    staticVotingObject = bot.get_cog('VotingClass')
    # print("Anzahl Argumente: " + str(number)) # Für Debuggin Zwecke: postet in Konsole Anzahl der Wahlmöglichkeiten

    # Abstimmungsmöglichkeiten an die Klasse übergeben: (addVotingOption() ist Member von VotingClass)
    # ctx.author liefert [NAME]#[NUMBER]
    await staticVotingObject.addVotingOptions(number, argumentList, ctx.author)

    # Fertig! Es kann los gehen.


# Beendet eine Abstimmung und entläd das entsprechende Cog (d.h. Kommandos die in VotingClass deklariert sind, funktionieren nicht mehr!)
@bot.command(name='CloseVoting', help="Beendet Abstimmung")
async def CloseVoting(ctx):
    global ongoingVote  # globale Variable

    # Erste prüfen ob überhaupt eine Abstimmung gestartet wurde:
    if ongoingVote == True:
        bot.unload_extension('VotingClass')
        ongoingVote = False  # ermöglicht wieder eine Abstimmung
        await ctx.send("Abstimmung beendet!")


# ##############################################
# ---------------WOHER-KOMME-ICH?---------------
# ##############################################
#
#
#
@bot.command(name='Computer_wer_hat_Sie_erschaffen?')
async def creator(ctx):
    await ctx.send(f"Das, mein Lieber {ctx.author.name}," +
                   "war der allseits bekannte und beliebte Programmierer" +
                   "Stefan Lindörfer im Jahre des Herrn 2020")


# ##############################################
# -------------FEHLERABFANGROUTINE--------------
# ##############################################
#
# Fängt Fehler ab (evtl. noch spezifizieren und Fehlerbeschreibung direkt posten)
#
#
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command...")


# ##############################################
# -------------------RUN IT---------------------
# ##############################################
#
# Discord Token darf nicht im Internet veröffentlicht werden. Daher:
# das Token in einem seperatem File speichern und diese in die .gitignore
# Datei aufnehmen, sodass keine Veröffentlichung stattfindet.

file_object = open(".token", "r")

token = file_object.read()

bot.run(token, bot=True, reconnect=True)
