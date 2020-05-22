import os

import discord


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Hallo'):
        await message.channel.send(f'Hallo {message.author}!')
        #await message.channel.send(message.author)

    if message.content.startswith('Tutorial'):
        await message.channel.send("Hallo Welt!")

# Discord Token darf nicht im Internet veröffentlicht werden. Daher:
# das Token in einem seperatem File speichern und diese in die .gitignore
# Datei aufnehmen, sodass keine Veröffentlichung erfolgt.

file_object = open( ".token", "r" )

token = file_object.read()

client.run(token)