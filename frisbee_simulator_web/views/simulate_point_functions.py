import random

from frisbee_simulator_web.models import PlayerPointStat


class TeamInPointSimulation:
    def __init__(self, tournamentTeam, point, teamInGameSimulation):
        super().__init__()
        self.tournamentTeam = tournamentTeam
        self.team = tournamentTeam.team
        self.point = point
        self.teamInGameSimulation = teamInGameSimulation
        self.coinFlipChoice = None
        if self.teamInGameSimulation.startPointWithDisc:
            self.startPointWithDisc = True
        else:
            self.startPointWithDisc = False
        if self.teamInGameSimulation.startFirstHalfWithDisc:
            self.startFirstHalfWithDisc = True
            self.startSecondHalfWithDisc = False
        else:
            self.startFirstHalfWithDisc = False
            self.startSecondHalfWithDisc = True
        self.score = 0
        self.oLineH1 = PlayerInPointSimulation(self.team, self.point, self.team.o_line_players.all()[0],
                                               self.teamInGameSimulation.oLineH1.gameStats)
        self.oLineH2 = PlayerInPointSimulation(self.team, self.point, self.team.o_line_players.all()[1],
                                               self.teamInGameSimulation.oLineH2.gameStats)
        self.oLineH3 = PlayerInPointSimulation(self.team, self.point, self.team.o_line_players.all()[2],
                                               self.teamInGameSimulation.oLineH3.gameStats)
        self.oLineC1 = PlayerInPointSimulation(self.team, self.point, self.team.o_line_players.all()[3],
                                               self.teamInGameSimulation.oLineC1.gameStats)
        self.oLineC2 = PlayerInPointSimulation(self.team, self.point, self.team.o_line_players.all()[4],
                                               self.teamInGameSimulation.oLineC2.gameStats)
        self.oLineC3 = PlayerInPointSimulation(self.team, self.point, self.team.o_line_players.all()[5],
                                               self.teamInGameSimulation.oLineC3.gameStats)
        self.oLineC4 = PlayerInPointSimulation(self.team, self.point, self.team.o_line_players.all()[6],
                                               self.teamInGameSimulation.oLineC4.gameStats)
        self.dLineH1 = PlayerInPointSimulation(self.team, self.point, self.team.d_line_players.all()[0],
                                               self.teamInGameSimulation.dLineH1.gameStats)
        self.dLineH2 = PlayerInPointSimulation(self.team, self.point, self.team.d_line_players.all()[1],
                                               self.teamInGameSimulation.dLineH2.gameStats)
        self.dLineH3 = PlayerInPointSimulation(self.team, self.point, self.team.d_line_players.all()[2],
                                               self.teamInGameSimulation.dLineH3.gameStats)
        self.dLineC1 = PlayerInPointSimulation(self.team, self.point, self.team.d_line_players.all()[3],
                                               self.teamInGameSimulation.dLineC1.gameStats)
        self.dLineC2 = PlayerInPointSimulation(self.team, self.point, self.team.d_line_players.all()[4],
                                               self.teamInGameSimulation.dLineC2.gameStats)
        self.dLineC3 = PlayerInPointSimulation(self.team, self.point, self.team.d_line_players.all()[5],
                                               self.teamInGameSimulation.dLineC3.gameStats)
        self.dLineC4 = PlayerInPointSimulation(self.team, self.point, self.team.d_line_players.all()[6],
                                               self.teamInGameSimulation.dLineC4.gameStats)
        self.benchH1 = PlayerInPointSimulation(self.team, self.point, self.team.bench_players.all()[0],
                                               self.teamInGameSimulation.benchH1.gameStats)
        self.benchH2 = PlayerInPointSimulation(self.team, self.point, self.team.bench_players.all()[1],
                                               self.teamInGameSimulation.benchH2.gameStats)
        self.benchH3 = PlayerInPointSimulation(self.team, self.point, self.team.bench_players.all()[2],
                                               self.teamInGameSimulation.benchH3.gameStats)
        self.benchC1 = PlayerInPointSimulation(self.team, self.point, self.team.bench_players.all()[3],
                                               self.teamInGameSimulation.benchC1.gameStats)
        self.benchC2 = PlayerInPointSimulation(self.team, self.point, self.team.bench_players.all()[4],
                                               self.teamInGameSimulation.benchC2.gameStats)
        self.benchC3 = PlayerInPointSimulation(self.team, self.point, self.team.bench_players.all()[5],
                                               self.teamInGameSimulation.benchC3.gameStats)
        self.benchC4 = PlayerInPointSimulation(self.team, self.point, self.team.bench_players.all()[6],
                                               self.teamInGameSimulation.benchC4.gameStats)
        self.oLinePlayers = [self.oLineH1, self.oLineH2, self.oLineH3, self.oLineC1, self.oLineC2, self.oLineC3,
                             self.oLineC4]
        self.dLinePlayers = [self.dLineH1, self.dLineH2, self.dLineH3, self.dLineC1, self.dLineC2, self.dLineC3,
                             self.dLineC4]
        self.benchPlayers = [self.benchH1, self.benchH2, self.benchH3, self.benchC1, self.benchC2, self.benchC3,
                             self.benchC4]
        self.allPlayers = [self.oLineH1, self.oLineH2, self.oLineH3, self.oLineC1, self.oLineC2, self.oLineC3,
                           self.oLineC4, self.dLineH1, self.dLineH2, self.dLineH3, self.dLineC1, self.dLineC2,
                           self.dLineC3, self.dLineC4, self.benchH1, self.benchH2, self.benchH3, self.benchC1,
                           self.benchC2, self.benchC3, self.benchC4]
        self.sevenOnField = None
        self.hasDisc = None

    def __str__(self):
        return self.team.location + ' ' + self.team.mascot


class PlayerInPointSimulation:
    def __init__(self, team, point, player, gameStats):
        super().__init__()
        self.team = team
        self.point = point
        self.player = player
        self.onOffense = None
        self.onDefense = None
        self.hasDisc = False
        self.playerGuarding = None
        self.guardingDisc = None
        self.guardingPlayerBeingThrownTo = None
        self.pointStats = PlayerStatsInPointSimulation(point=self.point, player=self.player)
        self.gameStats = gameStats

    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name


class PlayerStatsInPointSimulation:
    def __init__(self, point, player):
        super().__init__()
        self.point = point
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


class PointSimulation:
    def __init__(self, game, point, teamInGameSimulationOne, teamInGameSimulationTwo):
        super().__init__()
        self.game = game
        self.point = point
        self.teamInGameSimulationOne = teamInGameSimulationOne
        self.teamInGameSimulationTwo = teamInGameSimulationTwo
        # simulate by team rating variables:
        self.randomYardsThrown = None
        self.randomReceiver = None
        self.differenceInTeamsOverallRating = None
        self.determiner = None
        self.probabilityForWinner = None
        self.betterTeam = None
        # everything else
        self.throwStartingProbability = None
        self.teamInPointSimulationOne = TeamInPointSimulation(self.point.team_one, self.point,
                                                              self.teamInGameSimulationOne)
        self.teamInPointSimulationTwo = TeamInPointSimulation(self.point.team_two, self.point,
                                                              self.teamInGameSimulationTwo)
        self.sevenOnFieldForTeamOne = None
        self.sevenOnFieldForTeamTwo = None
        self.sevenOnFieldForOffense = None
        self.sevenOnFieldForDefense = None
        self.teamOnOffenseCurrently = None
        self.teamOnDefenseCurrently = None
        self.pointWinner = None
        self.pointLoser = None
        self.pointOver = False
        self.yardsGainedDownField = 0
        self.playerWithDisc = None
        self.playerBeingThrownTo = None
        self.playerGuardingDisc = None
        self.playerGuardingPlayerBeingThrownTo = None
        self.receiverOptions = None
        self.defenderOptions = None
        self.throwChoice = None
        self.probabilityThrowIsCompleted = None
        self.assistThrower = None
        self.goalScorer = None
        self.throwerNumber = None
        self.simulationType = 'player_rating'
        self.oLineOnField = None
        self.dLineOnField = None
        self.discCurrentLocation = None
        self.playDirection = None  # Positive means going from 0-> 70, Negative means going from 0<-70
        self.teamWithDiscToStartGame = None
        self.pointPrintStatement = ''

    def simulate_point(self):
        self.determine_who_starts_point_with_disc()
        if self.simulationType == 'player_rating':
            self.put_correct_players_on_field()
            self.determine_starting_disc_location_before_pull()
            self.determine_where_pull_is_caught()
            self.determine_who_catches_pull()
            self.simulate_point_by_player_rating()
            self.save_player_point_stats_in_database(self.game)
        else:
            self.calculate_difference_in_teams_overall_rating()
            self.calculate_probability_for_winner()
            self.simulate_point_by_team_rating()

    def determine_who_starts_point_with_disc(self):
        if self.teamInPointSimulationOne.startPointWithDisc:
            self.pointPrintStatement += (str(self.teamInPointSimulationOne.team.mascot) + ' starts with Disc \n')
            self.teamOnOffenseCurrently = self.teamInPointSimulationOne
            self.teamOnDefenseCurrently = self.teamInPointSimulationTwo
            self.teamInPointSimulationOne.hasDisc = True
        elif self.teamInPointSimulationTwo.startPointWithDisc:
            self.pointPrintStatement += (str(self.teamInPointSimulationTwo.team.mascot) + ' starts with Disc \n')
            self.teamOnOffenseCurrently = self.teamInPointSimulationTwo
            self.teamOnDefenseCurrently = self.teamInPointSimulationOne
            self.teamInPointSimulationTwo.hasDisc = True
        else:
            print('neither team starts with disc')

    def put_correct_players_on_field(self):
        use_bench_dline = (random.randint(1, 3) == 1)  # 1-in-3 chance to use bench

        if self.teamInPointSimulationOne.startPointWithDisc:
            self.teamInPointSimulationOne.sevenOnField = self.teamInPointSimulationOne.oLinePlayers
            self.teamInPointSimulationTwo.sevenOnField = (
                self.teamInPointSimulationTwo.benchPlayers if use_bench_dline
                else self.teamInPointSimulationTwo.dLinePlayers
            )
            self.sevenOnFieldForOffense = self.teamInPointSimulationOne.sevenOnField
            self.sevenOnFieldForDefense = self.teamInPointSimulationTwo.sevenOnField

        elif self.teamInPointSimulationTwo.startPointWithDisc:
            self.teamInPointSimulationOne.sevenOnField = (
                self.teamInPointSimulationOne.benchPlayers if use_bench_dline
                else self.teamInPointSimulationOne.dLinePlayers
            )
            self.teamInPointSimulationTwo.sevenOnField = self.teamInPointSimulationTwo.oLinePlayers
            self.sevenOnFieldForOffense = self.teamInPointSimulationTwo.sevenOnField
            self.sevenOnFieldForDefense = self.teamInPointSimulationOne.sevenOnField

        else:
            print('error with correct players on field')

    def determine_starting_disc_location_before_pull(self):
        # team catches in endzone at 0, then disc starts at 0, and is pulled to 70
        if self.playDirection == -1:
            self.discCurrentLocation = 0
        # team catches in endzone at 70, disc starts at 70, and is pulled to 0
        else:
            self.discCurrentLocation = 70

    def determine_who_catches_pull(self):
        self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1],
                                self.sevenOnFieldForOffense[2]]
        self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1],
                                self.sevenOnFieldForDefense[2]]
        self.randomReceiver = random.randint(0, 2)
        self.playerWithDisc = self.receiverOptions[self.randomReceiver]
        self.pointPrintStatement += (str(self.playerWithDisc) + ' is catching the pull \n')
        self.playerGuardingDisc = self.defenderOptions[self.randomReceiver]
        self.determine_receiver_options()
        self.determine_defender_options()

    def determine_where_pull_is_caught(self):
        if self.discCurrentLocation == 70:
            random_start = random.randint(-10, 15)
        else:
            random_start = random.randint(55, 80)
        self.discCurrentLocation = random_start
        self.pointPrintStatement += ('The pull was caught at: ' + str(self.discCurrentLocation) + ' yard line \n')

    def determine_receiver_options(self):
        self.pointPrintStatement += (
                str(self.playerWithDisc.player.last_name) + ' has the disc at this location: ' + str(
            self.discCurrentLocation) + ' yard line. ')
        self.receiverOptions = []
        if self.playerWithDisc == self.sevenOnFieldForOffense[0]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[1], self.sevenOnFieldForOffense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[1]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[2]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[3]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[4]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[5],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[5]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[1], self.sevenOnFieldForOffense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[6]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[6]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5]]
        else:
            print('something went wrong in determining receiver options')

    def determine_defender_options(self):
        if self.playerGuardingDisc == self.sevenOnFieldForDefense[0]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[1], self.sevenOnFieldForDefense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[1]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[2]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[3]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[4]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[5],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[5]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[1], self.sevenOnFieldForDefense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[6]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[6]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5]]

    def simulate_swing_throw(self):
        self.throwChoice = 'swing'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.swing_throw_offense + self.playerBeingThrownTo.player.handle_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.handle_cut_defense)
        self.randomYardsThrown = random.randint(-5, 5)
        self.simulate_result_of_throw()

    def simulate_under_throw(self):
        self.throwChoice = 'under'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.under_throw_offense + self.playerBeingThrownTo.player.under_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.under_cut_defense)
        self.randomYardsThrown = random.randint(5, 15)
        self.simulate_result_of_throw()

    def simulate_short_huck_throw(self):
        self.throwChoice = 'short_huck'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.short_huck_throw_offense + self.playerBeingThrownTo.player.short_huck_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.short_huck_cut_defense)
        self.randomYardsThrown = random.randint(15, 30)
        self.simulate_result_of_throw()

    def simulate_deep_huck_throw(self):
        self.throwChoice = 'deep_huck'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.deep_huck_throw_offense + self.playerBeingThrownTo.player.deep_huck_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.deep_huck_cut_defense)
        self.randomYardsThrown = random.randint(30, 70)
        self.simulate_result_of_throw()

    def simulate_result_of_throw(self):
        self.pointPrintStatement += (str(self.playerWithDisc.player.last_name) + ' tries to throw to: ' + str(
            self.playerBeingThrownTo.player.last_name) + ' for ' + str(
            self.randomYardsThrown) + 'yards \n')
        self.discCurrentLocation += self.randomYardsThrown * self.playDirection
        if self.probabilityThrowIsCompleted < self.throwStartingProbability:
            # play direction is either positive or negative
            self.pointPrintStatement += (str(self.teamOnOffenseCurrently.team.mascot) + ' completed ' + str(
                self.throwChoice) + ' at this location: ' + str(
                self.discCurrentLocation) + '\n')
            if self.discCurrentLocation < -20:
                # turnover, disc goes to goal line at location 0 and team 2 has disc
                self.discCurrentLocation = 0
                self.assign_completions(isCompletion=False)
                self.assign_throwaway_to_thrower()
                self.assign_turnovers_forced()
                self.switch_teams_due_to_turnover()
            elif (self.playDirection == 1) and (70 < self.discCurrentLocation < 90):
                self.assistThrower = self.playerWithDisc
                self.goalScorer = self.playerBeingThrownTo
                self.pointWinner = self.teamOnOffenseCurrently.tournamentTeam
                self.teamOnOffenseCurrently.teamInGameSimulation.score += 1
                self.pointLoser = self.teamOnDefenseCurrently.tournamentTeam
                self.discCurrentLocation = 0
                self.assign_completions(isCompletion=True)
                self.assign_completion_yardage()
                self.assign_goals_and_assists()
                self.pointPrintStatement += (str(self.teamOnOffenseCurrently.team.mascot) + 'Scored! ' + str(
                    self.assistThrower) + ' threw the assist to ' + str(self.goalScorer.player.last_name) + '\n')
                self.pointOver = True
            elif (self.playDirection == -1) and (-20 < self.discCurrentLocation < 0):
                self.assistThrower = self.playerWithDisc
                self.goalScorer = self.playerBeingThrownTo
                self.pointWinner = self.teamOnOffenseCurrently.tournamentTeam
                self.teamOnOffenseCurrently.teamInGameSimulation.score += 1
                self.pointLoser = self.teamOnDefenseCurrently.tournamentTeam
                self.discCurrentLocation = 0
                self.assign_completion_yardage()
                self.assign_goals_and_assists()
                self.assign_completions(isCompletion=True)
                self.pointPrintStatement += (str(self.teamOnOffenseCurrently.team.mascot) + 'Scored! ' + str(
                    self.assistThrower) + ' threw the assist to ' + str(self.goalScorer.player.last_name) + '\n')
                self.pointOver = True
            elif self.discCurrentLocation > 90:
                self.discCurrentLocation = 70
                self.assign_completions(isCompletion=False)
                self.assign_throwaway_to_thrower()
                self.assign_turnovers_forced()
                self.switch_teams_due_to_turnover()
            else:
                self.playerWithDisc.pointStats.throwingYards += self.randomYardsThrown
                self.playerBeingThrownTo.pointStats.receivingYards += self.randomYardsThrown
                self.playerWithDisc.gameStats.throwingYards += self.randomYardsThrown
                self.playerBeingThrownTo.gameStats.receivingYards += self.randomYardsThrown
                self.playerWithDisc = self.playerBeingThrownTo
                self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
        else:
            self.pointPrintStatement += (
                    str(self.teamOnOffenseCurrently.team.mascot) + ' dropped the throw at this location: at this location: ' + str(
                self.discCurrentLocation) + '\n')
            yards_added = self.randomYardsThrown * self.playDirection
            self.discCurrentLocation += yards_added
            # Disc still moves, even if it is dropped, have to handle if disc lands in middle of end zone
            # or way out of bounds
            if self.discCurrentLocation <= -20:
                # turnover, disc goes to goal line at location 0 and team 2 has disc
                self.discCurrentLocation = 0
            elif -20 < self.discCurrentLocation < 0:
                self.discCurrentLocation = 0
            elif 70 < self.discCurrentLocation < 90:
                self.discCurrentLocation = 70
            elif self.discCurrentLocation >= 90:
                self.discCurrentLocation = 70
            # throw was either dropped or thrown away
            self.assign_drops()
            self.switch_teams_due_to_turnover()

    def simulate_point_by_player_rating(self):
        # four pass options:
        # 1: swing for -5 to +5 yards (random number between 0-3
        # 2: under for 5 to 15 yards (random number between 4-6
        # 3: short huck for 15-30 yards (random number between 7-8)
        # 4: deep huck for 31-70 yards (cant go through end of end zone) (random number == 9-10
        # Probability of Turnover
        while not self.pointOver:
            # determine what throw is going to be thrown
            random_number = random.randint(0, 10)
            if random_number in [0, 1, 2, 3]:
                self.throwChoice = 'swing'
                self.throwStartingProbability = 90
                self.simulate_swing_throw()
            elif random_number in [4, 5, 6]:
                self.throwChoice = 'under'
                self.throwStartingProbability = 80
                self.simulate_under_throw()
            elif random_number in [7, 8]:
                self.throwChoice = 'short_huck'
                self.throwStartingProbability = 65
                self.simulate_short_huck_throw()
            elif random_number in [9, 10]:
                self.throwChoice = 'deep_huck'
                self.throwStartingProbability = 55
                self.simulate_deep_huck_throw()

    def switch_teams_due_to_turnover(self):
        if self.teamOnOffenseCurrently == self.teamInPointSimulationOne:
            self.teamOnOffenseCurrently = self.teamInPointSimulationTwo
            self.teamOnDefenseCurrently = self.teamInPointSimulationOne
            self.sevenOnFieldForOffense = self.teamInPointSimulationTwo.sevenOnField
            self.sevenOnFieldForDefense = self.teamInPointSimulationOne.sevenOnField
            self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
            self.playerGuardingDisc = self.receiverOptions[self.randomReceiver]
            self.pointPrintStatement += (
                    str(self.teamOnOffenseCurrently.team.mascot) + ' now has the disc at this location: ' + str(
                self.discCurrentLocation) + '\n')
        else:
            self.teamOnOffenseCurrently = self.teamInPointSimulationOne
            self.teamOnDefenseCurrently = self.teamInPointSimulationTwo
            self.sevenOnFieldForOffense = self.teamInPointSimulationOne.sevenOnField
            self.sevenOnFieldForDefense = self.teamInPointSimulationTwo.sevenOnField
            self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
            self.playerGuardingDisc = self.receiverOptions[self.randomReceiver]
            self.pointPrintStatement += (
                    str(self.teamOnOffenseCurrently.team.mascot) + ' now has the disc at this location: ' + str(
                self.discCurrentLocation) + '\n')
        self.flip_play_direction()

    def flip_play_direction(self):
        if self.playDirection == 1:
            newPlayDirection = -1
        else:
            newPlayDirection = 1
        self.playDirection = newPlayDirection

    def assign_completions(self, isCompletion):
        if self.throwChoice == 'swing':
            self.playerWithDisc.pointStats.swingPassesThrown += 1
            self.playerWithDisc.gameStats.swingPassesThrown += 1
            if isCompletion:
                self.playerWithDisc.pointStats.swingPassesCompleted += 1
                self.playerWithDisc.gameStats.swingPassesCompleted += 1
        elif self.throwChoice == 'under':
            self.playerWithDisc.pointStats.underPassesThrown += 1
            self.playerWithDisc.gameStats.underPassesThrown += 1
            if isCompletion:
                self.playerWithDisc.pointStats.underPassesCompleted += 1
                self.playerWithDisc.gameStats.underPassesCompleted += 1
        elif self.throwChoice == 'short_huck':
            self.playerWithDisc.pointStats.shortHucksThrown += 1
            self.playerWithDisc.gameStats.shortHucksThrown += 1
            if isCompletion:
                self.playerWithDisc.pointStats.shortHucksCompleted += 1
                self.playerWithDisc.gameStats.shortHucksCompleted += 1
        elif self.throwChoice == 'deep_huck':
            self.playerWithDisc.pointStats.deepHucksThrown += 1
            self.playerWithDisc.gameStats.deepHucksThrown += 1
            if isCompletion:
                self.playerWithDisc.pointStats.deepHucksCompleted += 1
                self.playerWithDisc.gameStats.deepHucksCompleted += 1

    def assign_throwaway_to_thrower(self):
        self.playerWithDisc.pointStats.throwaways += 1
        self.playerWithDisc.gameStats.throwaways += 1

    def assign_drops(self):
        self.playerBeingThrownTo.pointStats.drops += 1
        self.playerBeingThrownTo.gameStats.drops += 1

    def assign_completion_yardage(self):
        self.playerWithDisc.pointStats.throwingYards += self.randomYardsThrown
        self.playerBeingThrownTo.pointStats.receivingYards += self.randomYardsThrown
        self.playerWithDisc.gameStats.throwingYards += self.randomYardsThrown
        self.playerBeingThrownTo.gameStats.receivingYards += self.randomYardsThrown

    def assign_goals_and_assists(self):
        self.playerWithDisc.pointStats.assists += 1
        self.playerBeingThrownTo.pointStats.goals += 1
        self.playerWithDisc.gameStats.assists += 1
        self.playerBeingThrownTo.gameStats.goals += 1

    def assign_turnovers_forced(self):
        if self.throwChoice == 'swing':
            if (self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.swing_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.handle_cut_defense - self.playerBeingThrownTo.player.handle_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.assign_turnover_forced_to_player_guarding_disc()
            else:
                self.assign_turnover_forced_to_player_guarding_player_being_thrown_to()
        elif self.throwChoice == 'under':
            if (self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.under_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.under_cut_defense - self.playerBeingThrownTo.player.under_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.assign_turnover_forced_to_player_guarding_disc()
            else:
                self.assign_turnover_forced_to_player_guarding_player_being_thrown_to()
        elif self.throwChoice == 'short_huck':
            if (
                    self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.short_huck_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.short_huck_cut_defense - self.playerBeingThrownTo.player.short_huck_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.assign_turnover_forced_to_player_guarding_disc()
            else:
                self.assign_turnover_forced_to_player_guarding_player_being_thrown_to()
        elif self.throwChoice == 'deep_huck':
            if (
                    self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.deep_huck_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.deep_huck_cut_defense - self.playerBeingThrownTo.player.deep_huck_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.assign_turnover_forced_to_player_guarding_disc()
            else:
                self.assign_turnover_forced_to_player_guarding_player_being_thrown_to()

    def assign_turnover_forced_to_player_guarding_disc(self):
        self.playerGuardingDisc.pointStats.turnoversForced += 1
        self.playerGuardingDisc.gameStats.turnoversForced += 1

    def assign_turnover_forced_to_player_guarding_player_being_thrown_to(self):
        self.playerGuardingPlayerBeingThrownTo.pointStats.turnoversForced += 1
        self.playerGuardingPlayerBeingThrownTo.gameStats.turnoversForced += 1

    def simulate_point_by_team_rating(self):
        if self.teamInPointSimulationOne.startPointWithDisc:
            self.pointPrintStatement += (str(self.teamInPointSimulationOne.team.mascot) + 'has disc to start \n')
            self.sevenOnFieldForTeamOne = self.teamInPointSimulationOne.team.o_line_players
            self.sevenOnFieldForTeamTwo = self.teamInPointSimulationTwo.team.d_line_players
            self.sevenOnFieldForOffense = self.teamInPointSimulationOne.team.o_line_players
            self.sevenOnFieldForDefense = self.teamInPointSimulationTwo.team.d_line_players
            self.discCurrentLocation = 0
            if self.betterTeam == self.teamInPointSimulationOne:
                # Team 1 has better chance to hold as better team
                self.determiner = random.randint(1, 100)
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamInPointSimulationOne.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationTwo.tournamentTeam
                    self.point.teamInPointSimulationOne.score += 1
                    self.pointPrintStatement += (
                            str(self.teamInPointSimulationOne.team.mascot) + ' held as better team \n')
                # Team 2 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamInPointSimulationTwo.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationOne.tournamentTeam
                    self.point.teamInPointSimulationTwo.score += 1
                    self.pointPrintStatement += (
                            str(self.teamInPointSimulationTwo.team.mascot) + ' broke as the worse team \n')
            elif self.betterTeam == self.teamInPointSimulationTwo:
                # Team 1 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamInPointSimulationOne.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationTwo.tournamentTeam
                    self.point.teamInPointSimulationOne.score += 1
                    self.pointPrintStatement + (
                            str(self.teamInPointSimulationOne.team.mascot) + ' held as worse team \n ')
                # Team 2 breaks as the better team
                else:
                    self.pointWinner = self.teamInPointSimulationTwo.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationOne.tournamentTeam
                    self.point.teamInPointSimulationTwo.score += 1
                    self.pointPrintStatement += (
                            str(self.teamInPointSimulationTwo.team.mascot) + ' broke as the better team \n ')
        else:
            self.pointPrintStatement += (str(self.teamInPointSimulationTwo.team.mascot) + 'has disc to start \n')
            self.sevenOnFieldForTeamOne = self.teamInPointSimulationOne.team.d_line_players
            self.sevenOnFieldForTeamTwo = self.teamInPointSimulationTwo.team.o_line_players
            self.sevenOnFieldForOffense = self.teamInPointSimulationTwo.team.o_line_players
            self.sevenOnFieldForDefense = self.teamInPointSimulationOne.team.d_line_players
            self.discCurrentLocation = 70
            if self.betterTeam == self.teamInPointSimulationTwo:
                # Team 2 has better chance to hold as better team
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamInPointSimulationTwo.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationOne.tournamentTeam
                    self.point.teamInPointSimulationTwo.score += 1
                    self.pointPrintStatement += (
                            str(self.teamInPointSimulationTwo.team.mascot) + ' holds as the better team \n')
                # Team 1 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamInPointSimulationOne.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationTwo.tournamentTeam
                    self.point.teamInPointSimulationOne.score += 1
                    self.pointPrintStatement += (
                            str(self.teamInPointSimulationOne.team.mascot) + ' broke as the worse team \n')
            elif self.betterTeam == self.teamInPointSimulationOne:
                # Team 2 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamInPointSimulationTwo.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationOne.tournamentTeam
                    self.point.teamInPointSimulationTwo.score += 1
                    self.pointPrintStatement += (
                            str(self.teamInPointSimulationTwo.team.mascot) + ' holds as the worse team \n')
                # Team 1 breaks as the better team
                else:
                    self.pointWinner = self.teamInPointSimulationOne.tournamentTeam
                    self.pointLoser = self.teamInPointSimulationTwo.tournamentTeam
                    self.point.teamInPointSimulationOne.score += 1
                    self.pointPrintStatement += (
                            str(self.teamInPointSimulationOne.team.mascot) + ' breaks as better team \n')

    def calculate_difference_in_teams_overall_rating(self):
        if self.teamInPointSimulationOne.team.overall_rating > self.teamInPointSimulationTwo.team.overall_rating:
            self.betterTeam = self.teamInPointSimulationOne
            self.differenceInTeamsOverallRating = self.teamInPointSimulationOne.team.overall_rating - self.teamInPointSimulationTwo.team.overall_rating
        else:
            self.betterTeam = self.teamInPointSimulationTwo
            self.differenceInTeamsOverallRating = self.teamInPointSimulationTwo.team.overall_rating - self.teamInPointSimulationOne.team.overall_rating

    def calculate_probability_for_winner(self):
        self.probabilityForWinner = self.differenceInTeamsOverallRating + 50

    def save_player_point_stats_in_database(self, game):
        teams = [self.teamInPointSimulationOne, self.teamInPointSimulationTwo]
        for team in teams:
            for player in team.allPlayers:
                # player is of type PlayerInPointSimulation
                point = player.pointStats.point
                point.save()
                game.save()
                playerPointStats = PlayerPointStat.objects.create(
                    game=game,
                    point=player.pointStats.point,
                    player=player.pointStats.player,
                    goals=player.pointStats.goals,
                    assists=player.pointStats.assists,
                    swing_passes_thrown=player.pointStats.swingPassesThrown,
                    swing_passes_completed=player.pointStats.swingPassesCompleted,
                    under_passes_thrown=player.pointStats.underPassesThrown,
                    under_passes_completed=player.pointStats.underPassesCompleted,
                    short_hucks_thrown=player.pointStats.shortHucksThrown,
                    short_hucks_completed=player.pointStats.shortHucksCompleted,
                    deep_hucks_thrown=player.pointStats.deepHucksThrown,
                    deep_hucks_completed=player.pointStats.deepHucksCompleted,
                    throwing_yards=player.pointStats.throwingYards,
                    receiving_yards=player.pointStats.receivingYards,
                    turnovers_forced=player.pointStats.turnoversForced,
                    throwaways=player.pointStats.throwaways,
                    drops=player.pointStats.drops,
                    callahans=player.pointStats.callahans,
                    pulls=player.pointStats.pulls
                )
                playerPointStats.save()
