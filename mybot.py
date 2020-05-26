import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio

import datetime


# Instanz von Client. Verbindung zu Discord:
client = discord.Client()

bot = commands.Bot(command_prefix="!")

# Ein Event asynchron registrieren:
@bot.event
async def on_ready(): # on_ready wird aufgerufen, wenn der Bot sich eingeloggt hat
    print("We have logged in successfully as {0.user}".format(client))

@bot.command()
async def clean(ctx, *, content: commands.clean_content(use_nicknames=False)):
    await ctx.send(content)


# Extra Klassen für darauf folgendes Command
# sofern möglich, die Klasse in extra Datei auslagern!
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

#bot.run()

#@bot.command()
#async def leave(ctx):
#    await ctx.voice_client.disconnect()

@commands.command(name='a')
async def test(ctx):
    print("A a was printed!")
    await ctx.channel.send("A a was printed!");

bot.add_command(test)


# Postet die aktuelle Uhrzeit
@bot.command(name='time')
async def time(ctx):
    print("We recognized a command!")
    current_time = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M, %Y-%m-%d")
    await ctx.send(current_time)

#bot.add_command(Zeit)

# Joint einem Channel
@bot.command(name="join_channel", help="Makes the bot join a channel!", aliases=["join"])
async def join(ctx, arg):
    print("Joining channel " + arg)
    author = ctx.message.author
    channel = author.voice.voice_channel
    await channel.connect(reconnect=True)
#bot.add_command(join)



# Event on_message wird für jede eingehende Nachricht gefeuert
#@client.event
#async def on_message(message):
#    if message.author == client.user: # soll verhindern, dass der Bot auf Messages von sich selbst reagiert
#        return

    # Prüfen ob die Nachricht mit einem bestimmten Schlüsselwort beginnt:
#    if message.content.startswith('Hallo'):
#        await message.channel.send(f'Hallo {message.author}!')

#    if message.content.startswith('Tutorial'):
#        await message.channel.send("Hallo Welt!")

#    if message.content.startswith('oder LindBot?'):
#        await message.channel.send('Ja, du hast recht!')

#@client.event
#async def on_member_join():

#@bot.command(pass_context=True)
#async def join(ctx):
#    author = ctx.message.author
#    channel = author.voice_channel
#    await channel.connect()
    #await bot.join(channel)

# Fängt Fehler ab (evtl. noch spezifizieren und Fehlerbeschreibung direkt posten)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command...")


# Discord Token darf nicht im Internet veröffentlicht werden. Daher:
# das Token in einem seperatem File speichern und diese in die .gitignore
# Datei aufnehmen, sodass keine Veröffentlichung stattfindet.

file_object = open( ".token", "r" )

token = file_object.read()

bot.run( token )
#client.run(token)