from frisbee_simulator_web.models import Game, TournamentBracket, Tournament, TournamentPool


def setup_prequarterfinal_round_for_twenty_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_pools = TournamentPool.objects.filter(tournament=tournament)
    poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    teamsInWinnersBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolCSortedTeams[0], poolDSortedTeams[0],
                             poolASortedTeams[1], poolBSortedTeams[1], poolCSortedTeams[1], poolDSortedTeams[1],
                             poolASortedTeams[2], poolBSortedTeams[2], poolCSortedTeams[2], poolDSortedTeams[2]]
    winnersBracket = TournamentBracket.objects.create(tournament=tournament, number_of_teams=12,
                                                      bracket_type='Championship')
    winnersBracket.teams.set(teamsInWinnersBracket)
    winnersBracket.save()
    for i, team in enumerate(teamsInWinnersBracket, start=1):
        team.bracket_play_seed = i
        team.save()
    created_by = request.user.profile
    # Pool B2 v Pool C3
    prequarter_game_one = Game(team_one=poolBSortedTeams[1], team_two=poolCSortedTeams[2],
                               tournament=tournament,
                               game_type='Pre-Quarterfinal', created_by=created_by)
    # Pool C2 v B3
    prequarter_game_two = Game(team_one=poolCSortedTeams[1], team_two=poolBSortedTeams[2],
                               tournament=tournament,
                               game_type='Pre-Quarterfinal', created_by=created_by)
    # Pool D2 v A3
    prequarter_game_three = Game(team_one=poolDSortedTeams[1], team_two=poolASortedTeams[2],
                                 tournament=tournament,
                                 game_type='Pre-Quarterfinal', created_by=created_by)
    # Pool A2 v D3
    prequarter_game_four = Game(team_one=poolASortedTeams[1], team_two=poolDSortedTeams[2],
                                tournament=tournament,
                                game_type='Pre-Quarterfinal', created_by=created_by)
    prequarter_game_one.save()
    prequarter_game_two.save()
    prequarter_game_three.save()
    prequarter_game_four.save()
    prequarter_games = [prequarter_game_one, prequarter_game_two, prequarter_game_three, prequarter_game_four]
    tournament.pre_quarterfinal_round_initialized = True
    tournament.pre_quarterfinal_round_games.set(prequarter_games)
    tournament.save()


def setup_quarterfinal_round_for_twenty_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    winnerPrequarterFinalGames = tournament.pre_quarterfinal_round_games.all()
    winnerPrequarterFinalGameOne = winnerPrequarterFinalGames[0]
    winnerPrequarterFinalGameTwo = winnerPrequarterFinalGames[1]
    winnerPrequarterFinalGameThree = winnerPrequarterFinalGames[2]
    winnerPrequarterFinalGameFour = winnerPrequarterFinalGames[3]
    created_by = request.user.profile
    tournament_pools = TournamentPool.objects.filter(tournament=tournament)
    poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    teamsInWinnersBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolCSortedTeams[0], poolDSortedTeams[0],
                             winnerPrequarterFinalGameOne.winner, winnerPrequarterFinalGameTwo.winner,
                             winnerPrequarterFinalGameThree.winner, winnerPrequarterFinalGameFour.winner]
    winnersBracket = TournamentBracket.objects.create(tournament=tournament, number_of_teams=8,
                                                      bracket_type='Championship')
    winnersBracket.teams.set(teamsInWinnersBracket)
    winnersBracket.save()
    winnerQuarterFinalGameOne = Game(team_one=teamsInWinnersBracket[0],
                                     team_two=winnerPrequarterFinalGameOne.winner,
                                     tournament=tournament,
                                     game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameTwo = Game(team_one=teamsInWinnersBracket[1],
                                     team_two=winnerPrequarterFinalGameTwo.winner,
                                     tournament=tournament,
                                     game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameThree = Game(team_one=teamsInWinnersBracket[2],
                                       team_two=winnerPrequarterFinalGameThree.winner,
                                       tournament=tournament,
                                       game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameFour = Game(team_one=teamsInWinnersBracket[3],
                                      team_two=winnerPrequarterFinalGameFour.winner,
                                      tournament=tournament,
                                      game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameOne.save()
    winnerQuarterFinalGameTwo.save()
    winnerQuarterFinalGameThree.save()
    winnerQuarterFinalGameFour.save()
    for i, team in enumerate(teamsInWinnersBracket, start=1):
        team.bracket_play_seed = i
        team.save()
    winner_games = [winnerQuarterFinalGameOne, winnerQuarterFinalGameTwo, winnerQuarterFinalGameThree,
                    winnerQuarterFinalGameFour]
    tournament.quarterfinal_round_initialized = True
    tournament.quarterfinal_round_games.set(winner_games)
    tournament.save()


def setup_semifinal_round_for_twenty_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    winnerQuarterFinalGames = tournament.quarterfinal_round_games.all()
    winnerQuarterFinalGameOne = winnerQuarterFinalGames[0]
    winnerQuarterFinalGameTwo = winnerQuarterFinalGames[1]
    winnerQuarterFinalGameThree = winnerQuarterFinalGames[2]
    winnerQuarterFinalGameFour = winnerQuarterFinalGames[3]
    created_by = request.user.profile
    winnerSemiFinalGameOne = Game(team_one=winnerQuarterFinalGameOne.winner,
                                  team_two=winnerQuarterFinalGameTwo.winner,
                                  tournament=tournament,
                                  game_type='Semifinal', created_by=created_by)
    winnerSemiFinalGameTwo = Game(team_one=winnerQuarterFinalGameThree.winner,
                                  team_two=winnerQuarterFinalGameFour.winner,
                                  tournament=tournament,
                                  game_type='Semifinal', created_by=created_by)
    fifthPlaceSemiFinalGameOne = Game(team_one=winnerQuarterFinalGameOne.loser,
                                      team_two=winnerQuarterFinalGameTwo.loser,
                                      tournament=tournament,
                                      game_type='5th-Place Semifinal', created_by=created_by)
    fifthPlaceSemiFinalGameTwo = Game(team_one=winnerQuarterFinalGameThree.loser,
                                      team_two=winnerQuarterFinalGameFour.loser,
                                      tournament=tournament,
                                      game_type='5th-Place Semifinal', created_by=created_by)
    winnerSemiFinalGameOne.save()
    winnerSemiFinalGameTwo.save()
    fifthPlaceSemiFinalGameOne.save()
    fifthPlaceSemiFinalGameTwo.save()
    winnerGames = [winnerSemiFinalGameOne, winnerSemiFinalGameTwo, fifthPlaceSemiFinalGameOne,
                   fifthPlaceSemiFinalGameTwo]
    tournament.semifinal_round_initialized = True
    tournament.semifinal_round_games.set(winnerGames)
    tournament.save()
    prequarterFinalGames = tournament.pre_quarterfinal_round_games.all()
    prequarterFinalGameOne = prequarterFinalGames[0]
    prequarterFinalGameTwo = prequarterFinalGames[1]
    prequarterFinalGameThree = prequarterFinalGames[2]
    prequarterFinalGameFour = prequarterFinalGames[3]
    ninthPlaceSemiFinalGameOne = Game(team_one=prequarterFinalGameOne.loser,
                                      team_two=prequarterFinalGameFour.loser,
                                      tournament=tournament,
                                      game_type='9th-Place Semifinal', created_by=created_by)
    ninthPlaceSemiFinalGameTwo = Game(team_one=prequarterFinalGameTwo.loser,
                                      team_two=prequarterFinalGameThree.loser,
                                      tournament=tournament,
                                      game_type='9th-Place Semifinal', created_by=created_by)
    ninthPlaceSemiFinalGameOne.save()
    ninthPlaceSemiFinalGameTwo.save()
    tournament_pools = TournamentPool.objects.filter(tournament=tournament)
    poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    thirteenthPlaceSemiFinalGameOne = Game(team_one=poolASortedTeams[3],
                                           team_two=poolDSortedTeams[3],
                                           tournament=tournament,
                                           game_type='13th-Place Semifinal', created_by=created_by)
    thirteenthPlaceSemiFinalGameTwo = Game(team_one=poolBSortedTeams[3],
                                           team_two=poolCSortedTeams[3],
                                           tournament=tournament,
                                           game_type='13th-Place Semifinal', created_by=created_by)
    thirteenthPlaceSemiFinalGameOne.save()
    thirteenthPlaceSemiFinalGameTwo.save()
    seventeenthPlaceSemiFinalGameOne = Game(team_one=poolASortedTeams[4],
                                            team_two=poolDSortedTeams[4],
                                            tournament=tournament,
                                            game_type='17th-Place Semifinal', created_by=created_by)
    seventeenthPlaceSemiFinalGameTwo = Game(team_one=poolBSortedTeams[4],
                                            team_two=poolCSortedTeams[4],
                                            tournament=tournament,
                                            game_type='17th-Place Semifinal', created_by=created_by)
    seventeenthPlaceSemiFinalGameOne.save()
    seventeenthPlaceSemiFinalGameTwo.save()
    loserGames = [ninthPlaceSemiFinalGameOne, ninthPlaceSemiFinalGameTwo, thirteenthPlaceSemiFinalGameOne,
                  thirteenthPlaceSemiFinalGameTwo, seventeenthPlaceSemiFinalGameOne, seventeenthPlaceSemiFinalGameTwo]
    tournament.losers_semifinal_round_initialized = True
    tournament.losers_semifinal_round_games.set(loserGames)
    tournament.save()


def setup_final_round_for_twenty_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    winnerSemiFinalGames = tournament.semifinal_round_games.all()
    semiFinalGameOne = winnerSemiFinalGames[0]
    semiFinalGameTwo = winnerSemiFinalGames[1]
    fifthPlaceSemifinalGameOne = winnerSemiFinalGames[2]
    fifthPlaceSemifinalGameTwo = winnerSemiFinalGames[3]
    created_by = request.user.profile
    championshipGame = Game(team_one=semiFinalGameOne.winner, team_two=semiFinalGameTwo.winner,
                            tournament=tournament,
                            game_type='Championship', created_by=created_by)
    thirdPlaceGame = Game(team_one=semiFinalGameOne.loser, team_two=semiFinalGameTwo.loser,
                          tournament=tournament,
                          game_type='3rd-Place Final', created_by=created_by)
    fifthPlaceGame = Game(team_one=fifthPlaceSemifinalGameOne.winner, team_two=fifthPlaceSemifinalGameTwo.winner,
                          tournament=tournament,
                          game_type='5th-Place Final', created_by=created_by)
    seventhPlaceGame = Game(team_one=fifthPlaceSemifinalGameOne.loser, team_two=fifthPlaceSemifinalGameTwo.loser,
                            tournament=tournament,
                            game_type='7th-Place Final', created_by=created_by)
    championshipGame.save()
    thirdPlaceGame.save()
    fifthPlaceGame.save()
    seventhPlaceGame.save()
    winnerGames = [championshipGame, thirdPlaceGame, fifthPlaceGame, seventhPlaceGame]
    tournament.final_round_initialized = True
    tournament.final_round_games.set(winnerGames)
    tournament.save()
    loserSemiFinalGames = tournament.losers_semifinal_round_games.all()
    ninthPlaceSemiFinalGameOne = loserSemiFinalGames[0]
    ninthPlaceSemiFinalGameTwo = loserSemiFinalGames[1]
    thirteenthPlaceSemiFinalGameOne = loserSemiFinalGames[2]
    thirteenthPlaceSemiFinalGameTwo = loserSemiFinalGames[3]
    seventeenthPlaceSemiFinalGameOne = loserSemiFinalGames[4]
    seventeenthPlaceSemiFinalGameTwo = loserSemiFinalGames[5]
    ninthPlaceGame = Game(team_one=ninthPlaceSemiFinalGameOne.winner, team_two=ninthPlaceSemiFinalGameTwo.winner,
                          tournament=tournament,
                          game_type='9th-Place Final', created_by=created_by)
    eleventhPlaceGame = Game(team_one=ninthPlaceSemiFinalGameOne.loser, team_two=ninthPlaceSemiFinalGameTwo.loser,
                             tournament=tournament,
                             game_type='11th-Place Final', created_by=created_by)
    thirteenthPlaceGame = Game(team_one=thirteenthPlaceSemiFinalGameOne.winner,
                               team_two=thirteenthPlaceSemiFinalGameTwo.winner,
                               tournament=tournament,
                               game_type='13th-Place Final', created_by=created_by)
    fifteenthPlaceGame = Game(team_one=thirteenthPlaceSemiFinalGameOne.loser,
                              team_two=thirteenthPlaceSemiFinalGameOne.loser,
                              tournament=tournament,
                              game_type='15th-Place Final', created_by=created_by)
    seventeenthPlaceGame = Game(team_one=seventeenthPlaceSemiFinalGameOne.winner,
                                team_two=seventeenthPlaceSemiFinalGameTwo.winner,
                                tournament=tournament,
                                game_type='17th-Place Final', created_by=created_by)
    nineteenthPlaceGame = Game(team_one=seventeenthPlaceSemiFinalGameOne.loser,
                               team_two=seventeenthPlaceSemiFinalGameTwo.loser,
                               tournament=tournament,
                               game_type='19th-Place Final', created_by=created_by)
    ninthPlaceGame.save()
    eleventhPlaceGame.save()
    thirteenthPlaceGame.save()
    fifteenthPlaceGame.save()
    seventeenthPlaceGame.save()
    nineteenthPlaceGame.save()
    loserGames = [ninthPlaceGame, eleventhPlaceGame, thirteenthPlaceGame, fifteenthPlaceGame, seventeenthPlaceGame,
                  nineteenthPlaceGame]
    tournament.losers_final_round_initialized = True
    tournament.losers_final_round_games.set(loserGames)
    tournament.save()
