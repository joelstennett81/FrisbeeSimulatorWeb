import random

from frisbee_simulator_web.models import PlayerGameStat, Point
from frisbee_simulator_web.views.simulate_point_functions import PointSimulation


class TeamInGameSimulation:
    def __init__(self, tournamentTeam, game):
        super().__init__()
        self.tournamentTeam = tournamentTeam
        self.team = tournamentTeam.team
        self.game = game
        self.coinFlipChoice = None
        self.startPointWithDisc = None
        self.startFirstHalfWithDisc = None
        self.startSecondHalfWithDisc = None
        self.score = 0
        self.oLineH1 = PlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[0])
        self.oLineH2 = PlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[1])
        self.oLineH3 = PlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[2])
        self.oLineC1 = PlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[3])
        self.oLineC2 = PlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[4])
        self.oLineC3 = PlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[5])
        self.oLineC4 = PlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[6])
        self.dLineH1 = PlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[0])
        self.dLineH2 = PlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[1])
        self.dLineH3 = PlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[2])
        self.dLineC1 = PlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[3])
        self.dLineC2 = PlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[4])
        self.dLineC3 = PlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[5])
        self.dLineC4 = PlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[6])
        self.benchH1 = PlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[0])
        self.benchH2 = PlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[1])
        self.benchH3 = PlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[2])
        self.benchC1 = PlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[3])
        self.benchC2 = PlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[4])
        self.benchC3 = PlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[5])
        self.benchC4 = PlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[6])
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


class PlayerInGameSimulation:
    def __init__(self, team, game, player):
        super().__init__()
        self.team = team
        self.game = game
        self.player = player
        self.onOffense = None
        self.onDefense = None
        self.hasDisc = False
        self.playerGuarding = None
        self.guardingDisc = None
        self.guardingPlayerBeingThrownTo = None
        self.gameStats = PlayerStatsInGameSimulation(game=self.game, player=self.player)

    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name


class PlayerStatsInGameSimulation:
    def __init__(self, game, player):
        super().__init__()
        self.game = game
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


class GameSimulation:
    def __init__(self, tournament=None, game=None):
        super().__init__()
        self.tournament = tournament
        self.game = game
        self.playDirection = 0
        self.point = None
        self.pointSimulation = None
        self.isStartOfFirstHalf = None
        self.isStartOfSecondHalf = None
        self.isFirstQuarter = None
        self.isSecondQuarter = None
        self.isThirdQuarter = None
        self.isFourthQuarter = None
        self.isOvertime = None

        self.isStartOfFirstQuarter = None
        self.isStartOfSecondQuarter = None
        self.isStartOfThirdQuarter = None
        self.isStartOfFourthQuarter = None
        self.isStartOfOvertime = None
        self.playDirectionCoinFlipResult = None
        self.startWithDiscCoinFlipResult = None
        self.quarter = None
        self.total_game_time = 0

        self.teamInGameSimulationOne = TeamInGameSimulation(self.game.team_one, self.game)
        self.teamInGameSimulationTwo = TeamInGameSimulation(self.game.team_two, self.game)
        self.tournamentTeamOne = self.teamInGameSimulationOne.tournamentTeam
        self.tournamentTeamTwo = self.teamInGameSimulationTwo.tournamentTeam
        self.sevenOnFieldForTeamOne = self.teamInGameSimulationOne.team.o_line_players
        self.sevenOnFieldForTeamTwo = self.teamInGameSimulationTwo.team.d_line_players
        self.determiner = 0
        self.discLocationY = 0
        self.betterTeam = 0
        self.differenceInTeamsOverallRating = 0
        self.probabilityForWinner = 0
        self.winner = None
        self.loser = None
        self.pointWinner = None
        self.gameOver = False
        self.teamWithDiscToStartFirstHalf = None
        self.teamWithDiscToStartSecondHalf = None
        self.simulationType = 'player_rating'
        self.coinFlipResult = 0
        self.isFirstHalf = True
        self.isSecondHalf = False
        self.firstHalfPointsPlayed = 0
        self.secondHalfPointsPlayed = 0
        self.firstPointOfGamePlayDirection = 0
        self.pointCounter = 0
        self.pointSimulationsList = []

    def coin_flip(self):
        self.teamInGameSimulationOne.coinFlipChoice = 1
        self.teamInGameSimulationTwo.coinFlipChoice = 2
        self.startWithDiscCoinFlipResult = random.randint(1, 2)
        teamOneChoice = random.randint(1, 2)
        if teamOneChoice == self.startWithDiscCoinFlipResult:
            # team one won flip, receives disc to start
            self.teamWithDiscToStartFirstHalf = self.teamInGameSimulationOne
            self.teamWithDiscToStartSecondHalf = self.teamInGameSimulationTwo
        else:
            # team two won flip
            self.teamWithDiscToStartFirstHalf = self.teamInGameSimulationOne
            self.teamWithDiscToStartSecondHalf = self.teamInGameSimulationTwo
        self.playDirectionCoinFlipResult = random.randint(1, 2)
        if self.playDirectionCoinFlipResult == 1:
            self.playDirection = 1
        else:
            self.playDirection = -1
        self.firstPointOfGamePlayDirection = self.playDirection

    def simulate_point(self):
        if not self.isStartOfFirstHalf and not self.isStartOfSecondHalf:
            self.point = Point.objects.create(game=self.game, team_one=self.teamInGameSimulationOne.tournamentTeam,
                                              team_two=self.teamInGameSimulationTwo.tournamentTeam,
                                              point_number_in_game=self.pointCounter)
            self.point.save()
            self.pointSimulation = PointSimulation(self.game, self.point, self.teamInGameSimulationOne,
                                                   self.teamInGameSimulationTwo)
        self.pointSimulation.playDirection = self.playDirection
        self.pointSimulation.simulate_point()
        self.pointSimulationsList.append(self.pointSimulation)
        self.point.print_statements = self.pointSimulation.pointPrintStatement
        self.point.team_one_score_post_point = self.teamInGameSimulationOne.score
        self.point.team_two_score_post_point = self.teamInGameSimulationTwo.score
        self.point.winner = self.pointSimulation.pointWinner
        self.point.loser = self.pointSimulation.pointLoser
        self.point.save()
        self.point = None

    def simulate_ufa_point(self, current_quarter, total_game_time):
        if not self.isStartOfFirstHalf and not self.isStartOfSecondHalf:
            self.point = Point.objects.create(game=self.game, team_one=self.teamInGameSimulationOne.tournamentTeam,
                                              team_two=self.teamInGameSimulationTwo.tournamentTeam,
                                              point_number_in_game=self.pointCounter)
            self.point.save()
            self.pointSimulation = PointSimulation(self.game, self.point, self.teamInGameSimulationOne,
                                                   self.teamInGameSimulationTwo)
        self.pointSimulation.playDirection = self.playDirection
        time_of_point = self.pointSimulation.simulate_ufa_point(current_quarter, total_game_time)
        self.pointSimulationsList.append(self.pointSimulation)
        self.point.print_statements = self.pointSimulation.pointPrintStatement
        self.point.team_one_score_post_point = self.teamInGameSimulationOne.score
        self.point.team_two_score_post_point = self.teamInGameSimulationTwo.score
        self.point.winner = self.pointSimulation.pointWinner
        self.point.loser = self.pointSimulation.pointLoser
        self.point.save()
        self.point = None
        return time_of_point

    def simulate_full_game(self):
        self.pointCounter = 1
        self.setup_first_point_of_first_half()
        self.isFirstHalf = True
        self.isSecondHalf = False
        while not self.gameOver:
            self.simulate_point()
            if self.teamInGameSimulationOne.score == 15:
                self.winner = self.teamInGameSimulationOne.tournamentTeam
                self.loser = self.teamInGameSimulationTwo.tournamentTeam
                self.game.winner_score = self.teamInGameSimulationOne.score
                self.game.loser_score = self.teamInGameSimulationTwo.score
                self.gameOver = True
            elif self.teamInGameSimulationTwo.score == 15:
                self.winner = self.teamInGameSimulationTwo.tournamentTeam
                self.loser = self.teamInGameSimulationOne.tournamentTeam
                self.game.winner_score = self.teamInGameSimulationTwo.score
                self.game.loser_score = self.teamInGameSimulationOne.score
                self.gameOver = True
            else:
                self.setup_next_point()
            self.isStartOfFirstHalf = False
            self.isStartOfSecondHalf = False
        self.save_player_game_stats_in_database()

    def simulate_full_ufa_game(self):
        self.pointCounter = 1
        self.setup_first_point_of_period(1)
        self.isFirstHalf = True
        self.isSecondHalf = False
        self.quarter = 1
        while not self.gameOver:
            point_time = self.simulate_ufa_point(self.total_game_time, self.quarter)
            print('point time: ', point_time)
            self.total_game_time += point_time
            print('game time: ', self.total_game_time)
            print('quarter: ', self.quarter)
            if (self.quarter == 1) and (self.total_game_time > 720):
                print('reached end of first quarter')
                self.total_game_time = 720
                self.isFirstQuarter = False
                self.isSecondQuarter = True
                self.isStartOfSecondQuarter = True
                self.setup_first_point_of_period(2)
            elif (self.quarter == 2) and (self.total_game_time > 720):
                self.total_game_time = 1440
                self.isSecondQuarter = False
                self.isThirdQuarter = True
                self.isStartOfThirdQuarter = True
                self.isStartOfFirstHalf = False
                self.isStartOfSecondHalf = True
                self.setup_first_point_of_period(3)
            elif (self.quarter == 3) and (self.total_game_time > 720):
                self.total_game_time = 2160
                self.isThirdQuarter = False
                self.isFourthQuarter = True
                self.isStartOfFourthQuarter = True
                self.setup_first_point_of_period(4)
            elif (self.quarter == 4) and (self.total_game_time > 720):
                self.total_game_time = 2880
                self.isSecondQuarter = False
                self.isThirdQuarter = True
                if self.teamInGameSimulationOne.score == self.teamInGameSimulationTwo.score:
                    self.isFourthQuarter = False
                    self.isOvertime = True
                    self.isStartOfFirstHalf = False
                    self.isStartOfSecondHalf = False
                    self.isStartOfOvertime = True
                    self.setup_first_point_of_period(5)
                else:
                    if self.teamInGameSimulationOne.score > self.teamInGameSimulationTwo.score:
                        self.winner = self.teamInGameSimulationOne.tournamentTeam
                        self.loser = self.teamInGameSimulationTwo.tournamentTeam
                        self.game.winner_score = self.teamInGameSimulationOne.score
                        self.game.loser_score = self.teamInGameSimulationTwo.score
                        self.gameOver = True
                    else:
                        self.winner = self.teamInGameSimulationTwo.tournamentTeam
                        self.loser = self.teamInGameSimulationOne.tournamentTeam
                        self.game.winner_score = self.teamInGameSimulationTwo.score
                        self.game.loser_score = self.teamInGameSimulationOne.score
                        self.gameOver = True
            else:
                print('setting up next point')
                self.setup_next_ufa_point()
            self.isStartOfFirstHalf = False
            self.isStartOfSecondHalf = False
            self.isStartOfFourthQuarter = False
            self.isStartOfOvertime = False
        self.save_player_game_stats_in_database()

    def flip_play_direction(self):
        if self.playDirection == 1:
            newPlayDirection = -1
        else:
            newPlayDirection = 1
        self.playDirection = newPlayDirection

    def setup_next_point(self):
        if self.teamInGameSimulationOne.score == 8 and self.teamInGameSimulationTwo.score < 8:
            if self.isFirstHalf:
                self.setup_first_point_of_second_half()
                return
        elif self.teamInGameSimulationOne.score < 8 and self.teamInGameSimulationTwo.score == 8:
            if self.isFirstHalf:
                self.setup_first_point_of_second_half()
                return
        if self.pointWinner == self.teamInGameSimulationOne:
            self.teamInGameSimulationOne.startPointWithDisc = False
            self.teamInGameSimulationTwo.startPointWithDisc = True
        elif self.pointWinner == self.teamInGameSimulationTwo:
            self.teamInGameSimulationOne.startPointWithDisc = True
            self.teamInGameSimulationTwo.startPointWithDisc = False
        self.flip_play_direction()
        self.pointCounter += 1

    def setup_next_ufa_point(self):
        print('winner: ', self.pointWinner)
        if self.pointWinner == self.teamInGameSimulationOne:
            self.teamInGameSimulationOne.startPointWithDisc = False
            self.teamInGameSimulationTwo.startPointWithDisc = True
        elif self.pointWinner == self.teamInGameSimulationTwo:
            self.teamInGameSimulationOne.startPointWithDisc = True
            self.teamInGameSimulationTwo.startPointWithDisc = False
        else:
            print('point ended on time, not score')
        self.flip_play_direction()
        self.pointCounter += 1

    def setup_first_point_of_first_half(self):
        self.isFirstHalf = True
        self.isSecondHalf = False
        self.isStartOfFirstHalf = True
        self.isStartOfSecondHalf = False
        self.teamWithDiscToStartFirstHalf.startPointWithDisc = True
        self.teamWithDiscToStartFirstHalf.startFirstHalfWithDisc = True
        self.teamWithDiscToStartFirstHalf.startSecondHalfWithDisc = False
        self.teamWithDiscToStartFirstHalf.hasDisc = True
        self.teamWithDiscToStartSecondHalf.startFirstHalfWithDisc = False
        self.teamWithDiscToStartSecondHalf.startSecondHalfWithDisc = True
        self.teamWithDiscToStartSecondHalf.startPointWithDisc = False
        self.teamWithDiscToStartSecondHalf.hasDisc = False
        self.game.save()
        self.point = Point.objects.create(game=self.game, team_one=self.tournamentTeamOne,
                                          team_two=self.tournamentTeamTwo,
                                          point_number_in_game=self.pointCounter)
        self.point.save()
        self.pointSimulation = PointSimulation(self.game, self.point, self.teamInGameSimulationOne,
                                               self.teamInGameSimulationTwo)
        if self.firstPointOfGamePlayDirection == 1:
            # pull will go 70 -> 0, then play will go 0->70
            self.playDirection = 1
            self.pointSimulation.discPrePullLocation = 70
            self.pointSimulation.discCurrentLocation = 70
            self.pointSimulation.discPostGoalLocation = 70
        else:
            # pull will go 0 -> 70, then play will go 70->0
            self.playDirection = -1
            self.pointSimulation.discPrePullLocation = 0
            self.pointSimulation.discCurrentLocation = 0
            self.pointSimulation.discPostGoalLocation = 0

    def setup_first_point_of_period(self, period_number):
        print('setting up first point of period: ', period_number)
        # Reset all flags
        self.quarter = period_number
        self.isFirstQuarter = period_number == 1
        self.isSecondQuarter = period_number == 2
        self.isThirdQuarter = period_number == 3
        self.isFourthQuarter = period_number == 4
        self.isOvertime = period_number == 5

        self.isStartOfFirstQuarter = period_number == 1
        self.isStartOfSecondQuarter = period_number == 2
        self.isStartOfThirdQuarter = period_number == 3
        self.isStartOfFourthQuarter = period_number == 4
        self.isStartOfOvertime = period_number == 5

        self.total_game_time = 0

        # Decide which team starts with disc this period
        if period_number in (1, 4, 5):
            team_with_disc = self.teamWithDiscToStartFirstHalf
            team_without_disc = self.teamWithDiscToStartSecondHalf
        else:  # period 2 or 3
            team_with_disc = self.teamWithDiscToStartSecondHalf
            team_without_disc = self.teamWithDiscToStartFirstHalf

        team_with_disc.startPointWithDisc = True
        team_with_disc.hasDisc = True
        team_without_disc.startPointWithDisc = False
        team_without_disc.hasDisc = False

        # Set half possession flags
        team_with_disc.startFirstHalfWithDisc = period_number in (1, 4, 5)
        team_with_disc.startSecondHalfWithDisc = period_number == 3
        team_without_disc.startFirstHalfWithDisc = not team_with_disc.startFirstHalfWithDisc
        team_without_disc.startSecondHalfWithDisc = not team_with_disc.startSecondHalfWithDisc

        # Save game and create point
        self.game.save()
        self.point = Point.objects.create(
            game=self.game,
            team_one=self.tournamentTeamOne,
            team_two=self.tournamentTeamTwo,
            point_number_in_game=self.pointCounter
        )
        self.point.save()

        self.pointSimulation = PointSimulation(
            self.game, self.point,
            self.teamInGameSimulationOne, self.teamInGameSimulationTwo
        )

        # Set disc locations based on play direction
        if self.firstPointOfGamePlayDirection == 1:
            self.playDirection = 1
            self.pointSimulation.discPrePullLocation = 80
            self.pointSimulation.discCurrentLocation = 80
            self.pointSimulation.discPostGoalLocation = 80
        else:
            self.playDirection = -1
            self.pointSimulation.discPrePullLocation = 0
            self.pointSimulation.discCurrentLocation = 0
            self.pointSimulation.discPostGoalLocation = 0

        self.setup_next_ufa_point()

    def setup_first_point_of_second_half(self):
        self.isFirstHalf = False
        self.isSecondHalf = True
        self.isStartOfFirstHalf = False
        self.isStartOfSecondHalf = True
        self.teamWithDiscToStartSecondHalf.startPointWithDisc = True
        self.teamWithDiscToStartFirstHalf.startPointWithDisc = False
        self.point = Point.objects.create(game=self.game, team_one=self.tournamentTeamOne,
                                          team_two=self.tournamentTeamTwo,
                                          point_number_in_game=self.pointCounter)
        self.point.save()
        self.pointSimulation = PointSimulation(self.game, self.point, self.teamInGameSimulationOne,
                                               self.teamInGameSimulationTwo)
        if self.firstPointOfGamePlayDirection == 1:
            # pull will go 70 -> 0, then play will go 0->70
            self.playDirection = 1
            self.pointSimulation.discPrePullLocation = 70
            self.pointSimulation.discCurrentLocation = 70
            self.pointSimulation.discPostGoalLocation = 70
        else:
            # pull will go 0 -> 70, then play will go 70->0
            self.playDirection = -1
            self.pointSimulation.discPrePullLocation = 0
            self.pointSimulation.discCurrentLocation = 0
            self.pointSimulation.discPostGoalLocation = 0

    def save_player_game_stats_in_database(self):
        teams = [self.teamInGameSimulationOne, self.teamInGameSimulationTwo]
        for team in teams:
            for player in team.allPlayers:
                # player is of type PlayerInPointSimulation
                game = self.game
                game.save()
                playerGameStats = PlayerGameStat.objects.create(
                    tournament=self.tournament,
                    game=self.game,
                    player=player.gameStats.player,
                    goals=player.gameStats.goals,
                    assists=player.gameStats.assists,
                    swing_passes_thrown=player.gameStats.swingPassesThrown,
                    swing_passes_completed=player.gameStats.swingPassesCompleted,
                    under_passes_thrown=player.gameStats.underPassesThrown,
                    under_passes_completed=player.gameStats.underPassesCompleted,
                    short_hucks_thrown=player.gameStats.shortHucksThrown,
                    short_hucks_completed=player.gameStats.shortHucksCompleted,
                    deep_hucks_thrown=player.gameStats.deepHucksThrown,
                    deep_hucks_completed=player.gameStats.deepHucksCompleted,
                    throwing_yards=player.gameStats.throwingYards,
                    receiving_yards=player.gameStats.receivingYards,
                    turnovers_forced=player.gameStats.turnoversForced,
                    throwaways=player.gameStats.throwaways,
                    drops=player.gameStats.drops,
                    callahans=player.gameStats.callahans,
                    pulls=player.gameStats.pulls
                )
                playerGameStats.save()
