# Discord API
import discord
from discord.ext import commands

from VoteOption import VoteOption  # Objekt für Wahloption

# Stellt einen Cog dar, also eine Ansammlung von Kommandos und dient als
# Klasse zur Durchführung einer Abstimmung.


class VotingClass(commands.Cog):
    # GLOBALE VARIABLEN
    __Voters = {*()}  # Enthält alle, die ihre Stimme abgegeben haben
    __Options = {}  # Enthält ein Tupel aus key und value, wobei value das VoteOption-Objekt ist und key die fortlaufende Abstimmungsnummer

    def __init__(self, bot):  # Konstruktor
        self.bot = bot
        self.__Pause = False  # Keine Pause beim initialisieren!

        #print("Konstruktor wurde aufgerufen!")
        # self.__Organizer = organizer  # User der Abstimmung eingeleitet hat
    def __del__(self):  # Destruktor
        print("Destruktor wurde aufgerufen!")

    # speichert, wer die Abstimmung begonnen hat. Nur dieser hat Zugriff auf manche Kommandos  [ GERADE NOCH DEAKTIVIERT ]
    def setCreator(self, creator):
        self.__Organizer = creator

    # Allgemein:
    # Kommandos sind noch nicht final! Zum Ende hin, griffigere Begriffe einführen!

    # @commands.command(name='addVotingOption')
    # async def addVotingOption(self, ctx, option: str):
        # zuerst prüfen ob 'option' bereits im dict ist
    #    if option not in self.__Options.values():
        # neue Option hinzufügen:
    #        newOption = VoteOption(option)
        #self.__Options.update(self.countVoteOptions, newOption)
    #    else:
        # Option bereits vorhanden:
    #        await ctx.channel.send("- Option bereits vorhanden! -")

    # Diese Funktion wird ausschließlich durch das Kommando !Voting ... aufgerufen und erhält
    # als Parameter die Wahlmöglichkeiten. Es ist beabsichtigt, nachträglich weitere
    # Möglichkeiten hinzufügen bzw. entfernen zu können:
    def addVotingOptions(self, number: int, arguments):  # , *args):
        counter = 1  # Fortlaufende Nummer um Wahlmöglichkeiten durchzunumerieren

        # Iteriert durch die Liste (arguments)
        for x in arguments:
            # x ist ein String

            # neues VoteOption Objekt mit x anlegen:
            Option = VoteOption(x)

            # Objekt an counter-Stelle einfügen (counter steigt stetig, daher keine Rücksicht auf Überschreibungen etc.)
            self.__Options[counter] = Option

            # inkrementieren:
            counter += 1
    #
    #

    # Ermöglicht es einem User während einer Abstimmung seine Stimme für eine Wahlmöglichkeit abzugeben:
    @commands.command(name="Vote")
    async def Vote(self, ctx, option: int):
        # Zuerst prüfen ob eine Abstimmungspause gilt:
        if self.__Pause == True:
            await ctx.send("Stimmabgabe gerade nicht möglich!")
            return

        # Wenn jemand mittels Kommando abgestimmt hat, folgendes prüfen:
        # - Hat er bereits abgestimmt?
        # - Ist die Wahloption (option) gültig, also bildet sie auf ein Element im dict ab

        # Mit Hilfe von Mengenoperationen prüfen ob Abstimmender schon in der Wählerliste ist:
        if str(ctx.message.author) not in self.__Voters:
            # Hier: Hat noch nicht abgestimmt

            if option > 0 and option <= len(self.__Options):
                # Hier: Stimmabgabe bildet auf gültiges Element ab: Stimme ist gültig!

                # Stimme verbuchen:
                # dazu, dass option-te Element aus dict referenzieren:
                _VoteOption = self.__Options[option]
                # und Wert seiner Stimme inkrementieren:
                _VoteOption.votes += 1
            else:
                # Hat jemand eine Stimme abgegeben, die auf kein Element abbildet, eine Meldung
                # ausgeben, da es sich um ein versehen handeln könnte.
                await ctx.send(f"{ctx.author.name}, du hast für eine ungültige Option gestimmt, aber du bekommst noch eine Chance!")
        # else:
            # Hier: User hat schon einmal abgestimmt. Falls erforderlich, 'else:' entkommentieren und hier Vorkehrungen treffen:
            #print("Du hast schon einmal abgestimmt!")
    #
    #

    # Ermöglicht es dem Abstimmungsleiter, das Abstimmungsergebnis zu veröffentlichen. Dabei wird keine Rücksicht darauf
    # genommen, dass jeder anwesende User seine Stimme abgegeben hat.
    @commands.command(name="ShowResult")
    async def showResult(self, ctx):
        # Darf nur der User ausführen, der die Abstimmmung begonnen hat.
        # Beendet gleichzeit die Abstimmung und zerstört das Objekt

        # TODO: [ Hier fehlt noch eine Prüfung ob der User berechtigt ist, diese Funktion auszuführen! ]

        # 1.) Anzahl der Stimmen ermitteln, dazu durch gesamtes dict iterieren und Stimmen zählen
        anzahlgesamtstimmten = 0
        for x in self.__Options.values():
            anzahlgesamtstimmten += x.votes  # Stimmen jeder Wahloption aufaddieren

        # Obligatorische Prüfung ob Gesamtanzahl Stimmen gleich 0 ist.
        # Dann würde unten eine Division durch Null stehen. Hier dann
        # also abbrechen:
        if anzahlgesamtstimmten == 0:
            await ctx.send("Abgegebene Anzahl Stimmen: 0. Abbruch!")
            return

        # Im Anschluss, nochmals durch dict iterieren und jetzt das Stimmenverhältnis (Stimmen pro Option / Gesamtstimmen) ausrechnen
        # sowie den Gewinner bzw. ein Unentschieden feststellen

        # Enthält nacheinander gesamte Ausgabe, die am Schluss gepostet wird
        Zeichenkette = "__Ergebnis:__\n"

        # fortlaufende Nummer um Wahlmöglichkeiten korrekt darzustellen (kann nicht aus dict extrahiert werden, da hier nur durch values() und nicht durch keys() iteriert wird):
        counter = 1

        def AnzahlBalken(counter): return '@' * \
            counter  # gibt '#' genau i-Mal zurück

        # berechnet das Verhältnis der Stimmen der Wahlmöglichkeit geteilt durch Gesamtstimmen mal maximale Anzahl an Balkensymbolen
        def VerhältnisBalken(x, y, z): return round(x/y*z)

        # Standart: 0. Enthält die größte Zahl der Stimmen, die eine Option dieser Abstimmung gesammelt hat um einen Gewinner festzustellen:
        maxVotes = 0
        # Standart: 1. Speichert, ob eine zweite Option genau so viele Stimmen besitzt wie maxVotes, dann hat man ein Unentschieden zwischen mindestens 2 Optionen:
        sameResult = 1
        # Standart: 0. Speichert fortlaufende Nummer der Gewinneroption um nicht nachträglich noch einmal durch alle Optionen iterieren zu müssen:
        winner = 0
        # Speicher die Beschreibung des Gewinners für die Augabe (dicts können nicht wie ein Array abgefragt werden sondern man muss jedes mal durch sie iterieren):
        winner_desc = ""

        # durch dict iterieren und schrittweise Ausgabe erstellen sowie Gewinner feststellen:
        for x in self.__Options.values():
            # x ist jeweils ein VoteOption-Objekt

            # Stimmen der Wahloption bekommen:
            OptionStimmen = x.votes

            # Prüfen ob die aktuelle Option mehr Stimmen gesammelt hat als der bisherige "Gewinner" mit den meisten Stimmen:
            if OptionStimmen > maxVotes:
                maxVotes = OptionStimmen
                winner = counter
                sameResult = 1  # Entspricht 'Zurücksetzen'
                winner_desc = x.getDescription()
            elif OptionStimmen == maxVotes:
                sameResult += 1  # Es gibt eine zweite Option mit genauso vielen Stimmen

            # String für Ausgabe bilden, dazu mittels der beiden Lambda-Funktionen die Stärke des Balkens ermitteln:
            Zeichenkette += "***" + str(counter) + "***.)\t" + \
                "**" + str(AnzahlBalken(VerhältnisBalken(OptionStimmen, anzahlgesamtstimmten, 20))) + "**" \
                "\t(" + \
                str(OptionStimmen) + \
                ")" + \
                "\n"

            # inkrementieren für nächste Iteration:
            counter += 1

        # An dieser Stelle steht das Ergebnis fest. Daher jetzt noch eine Ausgabe für den Gewinner bzw. Unentschieden dran hängen:
        if sameResult == 1:
            # Es gibt einen eindeutigen Gewinner:
            Zeichenkette += "\n" + \
                "Der Gewinner ist: \t***" + \
                str(winner) + "***.) ***" + \
                str(winner_desc) + \
                "***\t   mit ***" + \
                str(maxVotes) + \
                "*** Stimmen!"
        else:
            # Es gibt keinen eindeutigen Gewinner, sondern ein Unentschieden zwischen mindestens zwei Optionen:
            Zeichenkette += "\n" + \
                "Hmm, es sieht so aus, als gäbe es ein Unentschieden?! Gleich nochmal abstimmen!"

        Zeichenkette += "\nAbgegebene Stimmen: **" + \
            str(anzahlgesamtstimmten) + "**"

        await ctx.send(Zeichenkette)  # Zeichenkette ausgeben
    #
    #

    # Ermöglichst es dem Abstimmungsleiter eine Pause der Stimmenabgabe zu bewirken.
    # So lange diese gilt, können von keinem User Stimmen abgegeben werden.
    @commands.command(name="PauseVoting")
    async def pauseVoting(self, ctx):
        # Pausiert die Abstimmung: Bisherige Stimmen bleiben erhalten
        # neue Abstimmungen aber unterbunden
        self.__Pause = True
        await ctx.channel.send("*Abstimmung wurde unterbrochen!*")
    #
    #

    # Erlaubt es von Seiten des Abstimmungsleiters wieder, Stimmen abzugeben.
    @commands.command(name="AllowVoting")
    async def allowVoting(self, ctx):
        # Erlaubt das Abstimmen wieder für alle
        self.__Pause = False
        await ctx.channel.send("*Abstimmung läuft wieder!*")
    #
    #

    # CLOSE VOTING WURDE IN DAS MAIN FILE VERSCHOBEN UM DAS COG WIEDER ENTLADEN ZU KÖNNEN. HIER WÜRDE DAS NÄMLICH NICHT FUNKTIONIEREN
    # @commands.command(name="CloseVoting")
    # async def closeVoting(self, ctx):
        # Schließt die Abstimmung: Weitere Stimmenabgaben sind nicht möglich
        # nun kann nur noch das Ergebnis verkündet werden
    #    if ctx.author.id == self.__Organizer:
        # Zuerst Stimmenabgabe unmöglich machen:
    #        self.__Pause = True

        # Dann: Ergebnis posten

        # self.bot.remove_cog('VotingClass')
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
