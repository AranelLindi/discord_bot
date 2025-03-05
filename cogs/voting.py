from discord.ext import commands

class _VoteOption:
    """ Hilfscontainer zur Speicherung einer Wahloption und deren Stimmenanzahl """
    def __init__(self, name: str):
        self.name = name
        self.votes = 0

class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ongoingVote = False
        self.voting_options = {}  # Speichert Optionen als {Nummer: _VoteOption}
        self.voters = set()  # Speichert Nutzer, die bereits abgestimmt haben

    async def cog_check(self, ctx):
        if not self.bot.active:
            return False
        return True

    @commands.command(name='Voting', help="Startet eine Abstimmung")
    async def voting(self, ctx, frage: str, *wahloptionen):
        if self.ongoingVote:
            await ctx.send("Es läuft bereits eine Abstimmung!")
            return

        if len(wahloptionen) < 2:
            await ctx.send("Du musst mindestens zwei Wahlmöglichkeiten festlegen!")
            return

        self.ongoingVote = True
        self.voting_options.clear()
        self.voters.clear()

        # Optionen speichern
        for i, option in enumerate(wahloptionen, start=1):
            self.voting_options[i] = _VoteOption(option)

        options_text = "\n".join([f"***{num}***) {opt.name}" for num, opt in self.voting_options.items()])
        await ctx.send(
            f"*Abstimmung gestartet von* __{ctx.author.name}__\n"
            f"**Thema:** ***{frage}***\n\n"
            f"__**Zur Auswahl stehen:**__\n{options_text}\n\n"
            "Stimme ab mit: `!Vote [Nr]`"
        )

    @commands.command(name='Vote', help="Gibt eine Stimme für eine Option ab")
    async def vote(self, ctx, option_number: int):
        if not self.ongoingVote:
            await ctx.send("Es läuft derzeit keine Abstimmung.")
            return

        if ctx.author.id in self.voters:
            await ctx.send(f"{ctx.author.name}, du hast bereits abgestimmt!")
            return

        if option_number not in self.voting_options:
            await ctx.send("Ungültige Wahloption!")
            return

        self.voting_options[option_number].votes += 1
        self.voters.add(ctx.author.id)
        await ctx.send(f"{ctx.author.name} hat für ***{self.voting_options[option_number].name}*** gestimmt!")

    @commands.command(name='ShowResults', help="Zeigt das aktuelle Abstimmungsergebnis")
    async def show_results(self, ctx):
        if not self.ongoingVote:
            await ctx.send("Es läuft derzeit keine Abstimmung.")
            return

        results_text = "\n".join(
            [f"***{num}***) {opt.name} - Stimmen: {opt.votes}" for num, opt in self.voting_options.items()]
        )

        await ctx.send(f"__**Zwischenstand der Abstimmung:**__\n{results_text}")

    @commands.command(name='CloseVoting', help="Beendet eine Abstimmung")
    async def close_voting(self, ctx):
        if not self.ongoingVote:
            await ctx.send("Es läuft derzeit keine Abstimmung.")
            return

        self.ongoingVote = False

        results_text = "\n".join(
            [f"***{num}***) {opt.name} - Stimmen: {opt.votes}" for num, opt in self.voting_options.items()]
        )
        await ctx.send(f"**Die Abstimmung wurde beendet!**\n__Endergebnis:__\n{results_text}")

async def setup(bot):
    await bot.add_cog(Voting(bot))
