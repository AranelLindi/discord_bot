# Discord API
import discord
from discord.ext import commands

from VoteOption import VoteOption  # Objekt für Wahloption

# Stellt einen Cog dar, also eine Ansammlung von Kommandos und dient als
# Klasse zur Durchführung einer Abstimmung.


class VotingClass(commands.Cog):
    # GLOBALE VARIABLEN
    __Voters = {*()}  # Enthält alle, die ihre Stimme abgegeben haben
    __Options = {}  # Enthält ein Tupel aus key und value, wobei value das VoteOption-Objekt ist

    def __init__(self, bot):  # Konstruktor
        self.bot = bot
        #self.countVoteOptions = 0
        print("Konstruktor wurde aufgerufen!")
        # self.__Organizer = organizer  # User der Abstimmung eingeleitet hat


    def __del__(self):
        print("Destruktor wurde aufgerufen!")

    # speichert, wer die Abstimmung begonnen hat. Nur dieser hat Zugriff auf manche Kommandos
    def setCreator(self, creator):
        self.__Organizer = creator

    # Allgemein:
    # Kommandos sind noch nicht final! Zum Ende hin, griffigere Begriffe einführen!

    #@commands.command(name='addVotingOption')
    #async def addVotingOption(self, ctx, option: str):
        # zuerst prüfen ob 'option' bereits im dict ist
    #    if option not in self.__Options.values():
            # neue Option hinzufügen:
    #        newOption = VoteOption(option)
            #self.__Options.update(self.countVoteOptions, newOption)
    #    else:
            # Option bereits vorhanden:
    #        await ctx.channel.send("- Option bereits vorhanden! -")
    def addVotingOption(self, number:int, arg:str):
        # Neues VoteOption Objekt mit arg (Abstimmungsbeschreibung) erstellen:
        Option = VoteOption(arg)

        # Ein Pair zusammen mit der fortlaufenden Nummer (NICHT Stimmenanzahl!) erstellen:
        pair = zip( number, Option )

        # Dem Dictionary das Pair hinzufügen:
        self.__Options.update(pair)
    #
    #

    @commands.command(name="Vote")
    async def voteFor(self, ctx, option: int):
        if self.__Pause == True:
            await ctx.channel.send("Stimmabgabe gerade nicht möglich!")
            return

        # Wenn jemand abgestimmt hat, folgendes prüfen:
        # - Hat er bereits abgestimmt?
        # - Ist die Wahloption (option) gültig, also bildet sie auf ein Element im dict ab

        # Mit Hilfe von Mengenoperationen prüfen ob Abstimmender schon in der Wählerliste ist:
        OneElementSet = set(ctx.message.author)
        if not OneElementSet.issubset(self.__Voters):
            # Hier: Hat noch nicht abgestimmt
            if self.__Options.keys()[option] is not None:
                # Hier: Stimmabgabe bildet auf gültiges Element ab: Stimme ist gültig!
                self.__Options.values()[option].addVote()
    #
    #

    @commands.command(name="ShowResult")
    async def showResult(self, ctx):
        # Darf nur der User ausführen, der die Abstimmmung begonnen hat.
        # Beendet gleichzeit die Abstimmung und zerstört das Objekt
        pass
    #
    #

    @commands.command(name="PauseVoting")
    async def pauseVoting(self, ctx):
        # Pausiert die Abstimmung: Bisherige Stimmen bleiben erhalten
        # neue Abstimmungen aber unterbunden
        self.__Pause = True
        await ctx.channel.send("*Abstimmung wurde unterbrochen!*")
    #
    #

    @commands.command(name="AllowVoting")
    async def allowVoting(self, ctx):
        # Erlaubt das Abstimmen wieder für alle
        self.__Pause = False
        await ctx.channel.send("*Abstimmung läuft wieder!*")
    #
    #

    #@commands.command(name="CloseVoting")
    #async def closeVoting(self, ctx):
        # Schließt die Abstimmung: Weitere Stimmenabgaben sind nicht möglich
        # nun kann nur noch das Ergebnis verkündet werden
    #    if ctx.author.id == self.__Organizer:
            # Zuerst Stimmenabgabe unmöglich machen:
    #        self.__Pause = True

            # Dann: Ergebnis posten

        #self.bot.remove_cog('VotingClass')
    #    teardown(self.bot) # Damit kann sich das Objekt selbst zerstören


# Aus der discord API Referenz:
# An extension (Anmerkung: Cog Extension) must have a global function, setup defined as the entry
# point on what to do when the extension is loaded. This entry point must have a single argument, the bot.
def setup(bot):
    bot.add_cog(VotingClass(bot))


# Nötig, falls das Cog nicht mehr gebraucht wird und entladen werden soll. Die Kommandos stehen
# dann nicht mehr zu Verfügung, bis eine neue Abstimmung erzeugt wurde.
def teardown(bot):
    bot.unload_extension(VotingClass(bot))