import random

from frisbee_simulator_web.models import *
from frisbee_simulator_web.views.ufa_simulate_point_functions import *


class UFATeamInGameSimulation:
    def __init__(self, seasonTeam, game):
        super().__init__()
        self.seasonTeam = seasonTeam
        self.team = seasonTeam.team
        self.game = game
        self.coinFlipChoice = None
        self.startPointWithDisc = None
        self.startFirstHalfWithDisc = None
        self.startSecondHalfWithDisc = None
        self.score = 0
        self.oLineH1 = UFAPlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[0])
        self.oLineH2 = UFAPlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[1])
        self.oLineH3 = UFAPlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[2])
        self.oLineC1 = UFAPlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[3])
        self.oLineC2 = UFAPlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[4])
        self.oLineC3 = UFAPlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[5])
        self.oLineC4 = UFAPlayerInGameSimulation(self.team, self.game, self.team.o_line_players.all()[6])
        self.dLineH1 = UFAPlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[0])
        self.dLineH2 = UFAPlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[1])
        self.dLineH3 = UFAPlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[2])
        self.dLineC1 = UFAPlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[3])
        self.dLineC2 = UFAPlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[4])
        self.dLineC3 = UFAPlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[5])
        self.dLineC4 = UFAPlayerInGameSimulation(self.team, self.game, self.team.d_line_players.all()[6])
        self.benchH1 = UFAPlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[0])
        self.benchH2 = UFAPlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[1])
        self.benchH3 = UFAPlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[2])
        self.benchC1 = UFAPlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[3])
        self.benchC2 = UFAPlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[4])
        self.benchC3 = UFAPlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[5])
        self.benchC4 = UFAPlayerInGameSimulation(self.team, self.game, self.team.bench_players.all()[6])
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


class UFAPlayerInGameSimulation:
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
        self.gameStats = UFAPlayerStatsInGameSimulation(game=self.game, player=self.player)

    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name


class UFAPlayerStatsInGameSimulation:
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


class UFAGameSimulation:
    def __init__(self, season=None, game=None):
        super().__init__()
        self.season = season
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

        self.teamInGameSimulationOne = UFATeamInGameSimulation(self.game.team_one, self.game)
        self.teamInGameSimulationTwo = UFATeamInGameSimulation(self.game.team_two, self.game)
        self.seasonTeamOne = self.teamInGameSimulationOne.seasonTeam
        self.seasonTeamTwo = self.teamInGameSimulationTwo.seasonTeam
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

    def simulate_ufa_point(self, current_quarter, total_game_time):
        if not self.isStartOfFirstQuarter and not self.isStartOfSecondQuarter and not self.isStartOfThirdQuarter and not self.isStartOfFourthQuarter:
            self.point = UFAPoint.objects.create(game=self.game, team_one=self.teamInGameSimulationOne.seasonTeam,
                                                 team_two=self.teamInGameSimulationTwo.seasonTeam,
                                                 point_number_in_game=self.pointCounter)
            self.point.save()
            self.pointSimulation = UFAPointSimulation(self.game, self.point, self.teamInGameSimulationOne,
                                                      self.teamInGameSimulationTwo, self.playDirection)
        self.pointSimulation.playDirection = self.playDirection
        time_of_point = self.pointSimulation.simulate_ufa_point(current_quarter, total_game_time)
        self.pointWinner = self.pointSimulation.pointWinner
        self.pointSimulationsList.append(self.pointSimulation)
        self.point.print_statements = self.pointSimulation.pointPrintStatement
        self.point.team_one_score_post_point = self.teamInGameSimulationOne.score
        self.point.team_two_score_post_point = self.teamInGameSimulationTwo.score
        self.point.winner = self.pointSimulation.pointWinner
        self.point.loser = self.pointSimulation.pointLoser
        self.point.save()
        self.point = None
        return time_of_point

    def simulate_full_ufa_game(self):
        self.pointCounter = 1
        self.setup_first_point_of_period(1)
        self.isFirstHalf = True
        self.isSecondHalf = False
        self.quarter = 1
        while not self.gameOver:
            point_time = self.simulate_ufa_point(self.total_game_time, self.quarter)
            self.total_game_time += point_time
            if (self.quarter == 1) and (self.total_game_time > 720):
                self.isFirstQuarter = False
                self.isSecondQuarter = True
                self.isStartOfSecondQuarter = True
                self.setup_first_point_of_period(2)
            elif (self.quarter == 2) and (self.total_game_time > 720):
                self.isSecondQuarter = False
                self.isThirdQuarter = True
                self.isStartOfThirdQuarter = True
                self.isStartOfFirstHalf = False
                self.isStartOfSecondHalf = True
                self.setup_first_point_of_period(3)
            elif (self.quarter == 3) and (self.total_game_time > 720):
                self.isThirdQuarter = False
                self.isFourthQuarter = True
                self.isStartOfFourthQuarter = True
                self.setup_first_point_of_period(4)
            elif (self.quarter == 4) and (self.total_game_time > 720):
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
                    print('score 1: ', self.teamInGameSimulationOne.score)
                    print('score 2: ', self.teamInGameSimulationTwo.score)
                    if self.teamInGameSimulationOne.score > self.teamInGameSimulationTwo.score:
                        print('in if')
                        self.winner = self.teamInGameSimulationOne.seasonTeam
                        self.loser = self.teamInGameSimulationTwo.seasonTeam
                        self.game.winner_score = self.teamInGameSimulationOne.score
                        self.game.loser_score = self.teamInGameSimulationTwo.score
                        self.gameOver = True
                    else:
                        print('in else')
                        self.winner = self.teamInGameSimulationTwo.seasonTeam
                        self.loser = self.teamInGameSimulationOne.seasonTeam
                        self.game.winner_score = self.teamInGameSimulationTwo.score
                        self.game.loser_score = self.teamInGameSimulationOne.score
                        self.gameOver = True
                    print('self.winner: ', self.winner)
                    print('self.loser: ', self.loser)
            elif (self.quarter == 5):
                if self.teamInGameSimulationOne.score > self.teamInGameSimulationTwo.score:
                    self.winner = self.teamInGameSimulationOne.seasonTeam
                    self.loser = self.teamInGameSimulationTwo.seasonTeam
                    self.game.winner_score = self.teamInGameSimulationOne.score
                    self.game.loser_score = self.teamInGameSimulationTwo.score
                    self.gameOver = True
                else:
                    self.winner = self.teamInGameSimulationTwo.seasonTeam
                    self.loser = self.teamInGameSimulationOne.seasonTeam
                    self.game.winner_score = self.teamInGameSimulationTwo.score
                    self.game.loser_score = self.teamInGameSimulationOne.score
                    self.gameOver = True
            else:
                self.setup_next_ufa_point()

            self.isStartOfFirstQuarter = False
            self.isStartOfSecondQuarter = False
            self.isStartOfThirdQuarter = False
            self.isStartOfFourthQuarter = False
            self.isStartOfOvertime = False
        self.save_player_game_stats_in_database()

    def flip_play_direction(self):
        if self.playDirection == 1:
            newPlayDirection = -1
        else:
            newPlayDirection = 1
        self.playDirection = newPlayDirection

    def setup_next_ufa_point(self):
        if self.pointWinner == self.teamInGameSimulationOne.seasonTeam:
            self.teamInGameSimulationOne.startPointWithDisc = False
            self.teamInGameSimulationTwo.startPointWithDisc = True
        elif self.pointWinner == self.teamInGameSimulationTwo.seasonTeam:
            self.teamInGameSimulationOne.startPointWithDisc = True
            self.teamInGameSimulationTwo.startPointWithDisc = False
        else:
            print('point ended on time, not score')
        self.flip_play_direction()
        self.pointCounter += 1

    def setup_first_point_of_period(self, period_number):
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
        self.point = UFAPoint.objects.create(
            game=self.game,
            team_one=self.seasonTeamOne,
            team_two=self.seasonTeamTwo,
            point_number_in_game=self.pointCounter
        )
        self.point.save()

        self.pointSimulation = UFAPointSimulation(
            self.game, self.point,
            self.teamInGameSimulationOne, self.teamInGameSimulationTwo, self.playDirection
        )

        # Set disc locations based on play direction
        if self.firstPointOfGamePlayDirection == 1:
            self.playDirection = 1
            self.pointSimulation.discCurrentLocation = 80
        else:
            self.playDirection = -1
            self.pointSimulation.discCurrentLocation = 0

    def save_player_game_stats_in_database(self):
        teams = [self.teamInGameSimulationOne, self.teamInGameSimulationTwo]
        for team in teams:
            for player in team.allPlayers:
                # player is of type PlayerInPointSimulation
                game = self.game
                game.save()
                playerGameStats = UFAPlayerGameStat.objects.create(
                    season=self.season,
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
