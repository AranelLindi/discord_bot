import discord

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

# Discord Token darf nicht im Internet veröffentlicht werden. Daher:
# den Token in einem seperatem File speichern und diese in die .gitignore
# Datei aufnehmen, sodass keine Veröffentlichung erfolgt.

file_object = open( "token.txt", "r" )

token = file_object.read()

client.run(token)