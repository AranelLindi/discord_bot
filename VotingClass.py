# Discord API
import discord
from discord.ext import commands

from VoteOption import VoteOption  # Objekt für Wahloption

# Stellt einen Cog dar, also eine Ansammlung von Kommandos und dient als Klasse zur Durchführung einer Abstimmung.


class VotingClass(commands.Cog):
    # GLOBALE VARIABLEN
    __voters = {*()}  # Enthält alle, die ihre Stimme abgegeben haben
    __options = {}  # Enthält ein Tupel aus key und value, wobei value das VoteOption-Objekt ist und key die fortlaufende Abstimmungsnummer

    def __init__(self, bot):  # Konstruktor
        self.bot = bot
        self.__pause = False  # Keine Abstimmungspause beim Initialisieren

    # def __del__(self):  # Destruktor # Wird aktuell nicht benötigt, hat aber funkionert, er wird aufgerufen.
        # print("Destruktor wurde aufgerufen!") # Hat funktioniert!


# ############################
#       HILFSFUNKTIONEN
# ############################

    # Diese Funktion wird ausschließlich durch das Kommando !Voting ... aufgerufen und erhält als Parameter die Wahlmöglichkeiten und den Abstimmungsersteller:

    def addVotingOptions(self, number: int, arguments, organizer: str):
        # Name des Abstimmunsgleiters speichern:
        self.organizer = organizer

        counter = 1  # Fortlaufende Nummer um Wahlmöglichkeiten durchzunumerieren

        # Iteriert durch die Liste (arguments)
        for x in arguments:
            # x ist ein String

            # neues VoteOption Objekt mit x anlegen:
            option = VoteOption(x)

            # Objekt an counter-Stelle einfügen (counter steigt stetig, daher keine Rücksicht auf Überschreibungen etc.)
            self.__options[counter] = option

            # inkrementieren:
            counter += 1

    # Vergleicht den übergebenen User (ctx.message.author) mit dem Namen des Abstimmungserstellers und gibt True oder False zurück:

    def permission(self, user):
        return self.organizer == user

# #####################
#       KOMMANDOS
# #####################


#   #####################
#           VOTE
#   #####################

    # Ermöglicht es einem User während einer Abstimmung seine Stimme für eine Wahlmöglichkeit abzugeben:

    @commands.command(name="Vote")
    async def Vote(self, ctx, option: int):
        # Zuerst prüfen ob eine Abstimmungspause gilt:
        if self.__pause == True:
            await ctx.send("*Stimmabgabe gerade nicht möglich!*")
            return

        # Wenn jemand mittels Kommando abgestimmt hat, folgendes prüfen:
        # - Hat er bereits abgestimmt?
        # - Ist die Wahloption (option) gültig, also bildet sie auf ein Element im dict ab

        # Mit Hilfe von Mengenoperationen prüfen ob Abstimmender schon in der Wählerliste ist:
        if str(ctx.message.author) not in self.__voters:
            # Hier: Hat noch nicht abgestimmt

            if option > 0 and option <= len(self.__options):
                # Hier: Stimmabgabe bildet auf gültiges Element ab: Stimme ist gültig!

                # Stimme verbuchen. Dazu, das option-te Element aus dict referenzieren...
                _VoteOption = self.__options[option]
                # ...und Wert seiner Stimme inkrementieren:
                _VoteOption.votes += 1

                # anschließend: Wähler in Liste aufnehmen:
                # TODO Umsetzen nachdem alles getestet wurde
            else:
                # Hat jemand eine Stimme (Zahl) abgegeben, die auf kein Element abbildet, eine Meldung ausgeben, da es sich um ein versehen handeln könnte.
                await ctx.send(f"{ctx.author.name}, Du hast für eine ungültige Option gestimmt, aber Du bekommst noch eine Chance!")
        else:
            # Hier: User hat schon einmal abgestimmt. Falls erforderlich, 'else:' entkommentieren und hier Vorkehrungen treffen:
            await ctx.send(f"{ctx.author.name}, Du Schlingel hast bereits deine Stimme abgegeben!")


#   ##########################
#           SHOW RESULT
#   ##########################

    # Ermöglicht es dem Abstimmungsleiter, das Abstimmungsergebnis zu veröffentlichen. Dabei wird keine Rücksicht darauf genommen, dass jeder anwesende User seine Stimme abgegeben hat.

    @commands.command(name="ShowResult")
    async def showResult(self, ctx):
        # Darf nur der User ausführen, der die Abstimmmung begonnen hat. Beendet gleichzeit die Abstimmung und zerstört das Objekt

        # TODO: [ Hier fehlt noch eine Prüfung ob der User berechtigt ist, diese Funktion auszuführen! ]
        # TESTEN!:
        # if ctx.message.author != self.organizer: # POTENZIELLE FEHLERQUELLE: Namensformat nicht sichergestellt. [NAME]#[NUMBER] od. [NAME] - Gerade funktioniert es, aber weiter testen!
        #    print("Fehler, ungültige Namen!")
        #    return
        if not self.permission(ctx.message.author):
            return

        # 1.) Anzahl der Stimmen ermitteln, dazu durch gesamtes dict iterieren und Stimmen zählen
        anzahlGesamtstimmten = 0
        for x in self.__options.values():
            anzahlGesamtstimmten += x.votes  # Stimmen jeder Wahloption aufaddieren

        # Obligatorische Prüfung ob Gesamtanzahl Stimmen gleich 0 ist. Dann würde unten eine Division durch Null stehen. Hier dann also abbrechen:
        if anzahlGesamtstimmten == 0:
            await ctx.send("Abgegebene Anzahl Stimmen: 0. Abbruch!")
            return

        # Im Anschluss, nochmals durch dict iterieren und jetzt das Stimmenverhältnis (Stimmen pro Option / Gesamtstimmen) ausrechnen
        # sowie den Gewinner bzw. ein Unentschieden feststellen

        # Enthält nacheinander gesamte Ausgabe, die am Schluss gepostet wird
        zeichenkette = "__Ergebnis:__\n"

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
        for x in self.__options.values():
            # x ist jeweils ein VoteOption-Objekt

            # Stimmen der Wahloption bekommen:
            option_stimmen = x.votes  # DAS HAT FUNKTIONIERT!

            # Prüfen ob die aktuelle Option mehr Stimmen gesammelt hat als der bisherige "Gewinner" mit den meisten Stimmen:
            if option_stimmen > maxVotes:
                maxVotes = option_stimmen
                winner = counter
                sameResult = 1  # Entspricht 'Zurücksetzen'
                winner_desc = x.name  # x.getDescription()
            elif option_stimmen == maxVotes:
                sameResult += 1  # Es gibt eine zweite Option mit genauso vielen Stimmen

            # String für Ausgabe bilden, dazu mittels der beiden Lambda-Funktionen die Stärke des Balkens ermitteln:
            darstellung = AnzahlBalken(VerhältnisBalken(
                option_stimmen, anzahlGesamtstimmten, 20))

            # Vermeidet Schönheitsfehler bei der Ausgabe, da bei leerem String die Zeichen für Fettschreibweise ** sonst geprintet würden:
            if len(darstellung) == 0:
                darstellung = ' '

            zeichenkette += "***" + str(counter) + "***.)\t" + \
                "**" + str(darstellung) + "**" \
                "\t(" + \
                str(option_stimmen) + \
                ")" + \
                "\n"

            # inkrementieren für nächste Iteration:
            counter += 1

        # An dieser Stelle steht das Ergebnis fest. Daher jetzt noch eine Ausgabe für den Gewinner bzw. Unentschieden dran hängen:
        if sameResult == 1:
            # Es gibt einen eindeutigen Gewinner:
            zeichenkette += "\n" + \
                "Der Gewinner ist: \t***" + \
                str(winner) + "***.) ***" + \
                str(winner_desc) + \
                "***\t   mit ***" + \
                str(maxVotes) + \
                "*** Stimmen!"
        else:
            # Es gibt keinen eindeutigen Gewinner, sondern ein Unentschieden zwischen mindestens zwei Optionen:
            zeichenkette += "\n" + \
                "Hmm, es sieht so aus, als gäbe es ein Unentschieden?! Stichwahl!?"

        zeichenkette += "\nAbgegebene Stimmen: **" + \
            str(anzahlGesamtstimmten) + "**"

        # Erklären wie die Abstimmung geschlossen wird:
        zeichenkette += "\nAbstimmung schließen mit: !CloseVoting"

        await ctx.send(zeichenkette)  # Zeichenkette ausgeben

    # Ermöglichst es dem Abstimmungsleiter eine Pause der Stimmenabgabe zu bewirken. So lange diese gilt, können von keinem User Stimmen abgegeben werden.


#   ######################
#           PAUSE
#   ######################

    # Pausiert die Abstimmung: Bisherige Stimmen bleiben erhalten neue Abstimmungen werden aber unterbunden

    @commands.command(name="Pause", help="Pausiert die Abstimmung")
    async def pause(self, ctx):

        # Darf nur der Abstimmungsleiter, daher prüfen
        if not self.permission(ctx.message.author):
            return

        self.__pause = True
        await ctx.channel.send("*Abstimmung wurde unterbrochen!*")


#   #########################
#           CONTINUE
#   #########################

    # Erlaubt es von Seiten des Abstimmungsleiters wieder, Stimmen abzugeben.

    @commands.command(name="Continue", help="Abstimmung weiterführen")
    async def cont(self, ctx):
        # Erlaubt das Abstimmen wieder für alle
        # Darf nur der Abstimmungsleiter, daher prüfen
        if not self.permission(ctx.message.author):
            return

        self.__pause = False
        await ctx.channel.send("*Abstimmung läuft wieder!*")

# ################################
#       DISCORD REGLEMENT
# ################################


# Zur Info, falls benötigt: Wie man ein Cog wieder entläd
# self.bot.remove_cog('VotingClass')
# teardown(self.bot) # Damit kann sich das Objekt selbst zerstören


# Aus der discord API Referenz:
# An extension (Anmerkung: Cog Extension) must have a global function, setup defined as the entry point on what to do when the extension is loaded. This entry point must have a single argument, the bot.
def setup(bot):
    # ruft gleichzeitig den Konstruktor von VotingClass auf
    bot.add_cog(VotingClass(bot))


# Nötig, falls das Cog nicht mehr gebraucht wird und entladen werden soll. Die Kommandos stehen dann nicht mehr zu Verfügung, bis eine neue Abstimmung erzeugt wurde.
def teardown(bot):
    # ruft gleichzeitig den Destruktor von VotingClass auf
    bot.unload_extension(VotingClass(bot))
