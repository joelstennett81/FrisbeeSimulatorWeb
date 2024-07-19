


class PlayerTournamentStatsInGameSimulation:
    def __init__(self, tournament, player):
        super().__init__()
        self.tournament = tournament
        self.player = player
        self.goals = 0
        self.assists = 0
        self.swingPassesThrown = 0
        self.swingPassesCompleted = 0
        self.underPassesThrown = 0
        self.underPassesCompleted = 0
        self.shortHucksThrown = 0
        self.shortHucksCompleted = 0
        self.deepHucksThrown = 0
        self.deepHucksCompleted = 0
        self.throwingYards = 0
        self.receivingYards = 0
        self.turnoversForced = 0
        self.throwaways = 0
        self.drops = 0
        self.callahans = 0
        self.pulls = 0
