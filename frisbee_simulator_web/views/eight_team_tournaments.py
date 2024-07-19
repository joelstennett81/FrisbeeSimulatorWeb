from frisbee_simulator_web.models import Game, TournamentBracket, Tournament, TournamentPool


def setup_quarterfinal_round_for_8_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    poolA = TournamentPool.objects.get(tournament=tournament, name='Pool A')
    poolB = TournamentPool.objects.get(tournament=tournament, name='Pool B')
    poolASortedTeams = poolA.teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = poolB.teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    # poolA1 v pool B4, pool B2vA3, pool B1vA4, pool A2vB3
    teamsInBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolASortedTeams[1], poolBSortedTeams[1],
                      poolASortedTeams[2], poolBSortedTeams[2], poolASortedTeams[3], poolBSortedTeams[3]]
    tournament_bracket = TournamentBracket.objects.create(tournament=tournament, number_of_teams=8,
                                                          bracket_type='Championship')
    tournament_bracket.teams.set(teamsInBracket)
    tournament_bracket.save()
    for i, team in enumerate(teamsInBracket, start=1):
        team.bracket_play_seed = i
        team.save()
    teams_in_bracket = tournament_bracket.teams.all()
    created_by = request.user.profile
    game_one = Game(team_one=teams_in_bracket[0], team_two=teams_in_bracket[7],
                    tournament=tournament_bracket.tournament,
                    game_type='Quarterfinal', created_by=created_by)
    game_two = Game(team_one=teams_in_bracket[1], team_two=teams_in_bracket[6],
                    tournament=tournament_bracket.tournament,
                    game_type='Quarterfinal', created_by=created_by)
    game_three = Game(team_one=teams_in_bracket[2], team_two=teams_in_bracket[5],
                      tournament=tournament_bracket.tournament,
                      game_type='Quarterfinal', created_by=created_by)
    game_four = Game(team_one=teams_in_bracket[3], team_two=teams_in_bracket[4],
                     tournament=tournament_bracket.tournament,
                     game_type='Quarterfinal', created_by=created_by)
    game_one.save()
    game_two.save()
    game_three.save()
    game_four.save()
    games = [game_one, game_two, game_three, game_four]
    tournament.quarterfinal_round_initialized = True
    tournament.quarterfinal_round_games.set(games)
    tournament.save()


def setup_semifinal_round_for_eight_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    quarterFinalGames = tournament.quarterfinal_round_games.all()
    quarterFinalGameOne = quarterFinalGames[0]
    quarterFinalGameTwo = quarterFinalGames[1]
    quarterFinalGameThree = quarterFinalGames[2]
    quarterFinalGameFour = quarterFinalGames[3]
    created_by = request.user.profile
    semiFinalGameOne = Game(team_one=quarterFinalGameOne.winner, team_two=quarterFinalGameTwo.winner,
                            tournament=tournament,
                            game_type='Semifinal', created_by=created_by)
    semiFinalGameTwo = Game(team_one=quarterFinalGameThree.winner, team_two=quarterFinalGameFour.winner,
                            tournament=tournament,
                            game_type='Semifinal', created_by=created_by)
    loserSemiFinalGameOne = Game(team_one=quarterFinalGameOne.loser, team_two=quarterFinalGameTwo.loser,
                                 tournament=tournament,
                                 game_type='5th-Place Semifinal', created_by=created_by)
    loserSemiFinalGameTwo = Game(team_one=quarterFinalGameThree.loser, team_two=quarterFinalGameFour.loser,
                                 tournament=tournament,
                                 game_type='5th-Place Semifinal', created_by=created_by)
    semiFinalGameOne.save()
    semiFinalGameTwo.save()
    loserSemiFinalGameOne.save()
    loserSemiFinalGameTwo.save()
    games = [semiFinalGameOne, semiFinalGameTwo, loserSemiFinalGameOne, loserSemiFinalGameTwo]
    tournament.semifinal_round_initialized = True
    tournament.semifinal_round_games.set(games)
    tournament.save()


def setup_final_round_for_eight_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    semiFinalGames = tournament.semifinal_round_games.all()
    semiFinalGameOne = semiFinalGames[0]
    semiFinalGameTwo = semiFinalGames[1]
    loserSemiFinalGameOne = semiFinalGames[2]
    loserSemiFinalGameTwo = semiFinalGames[3]
    created_by = request.user.profile
    championshipGame = Game(team_one=semiFinalGameOne.winner, team_two=semiFinalGameTwo.winner,
                            tournament=tournament,
                            game_type='Championship', created_by=created_by)
    thirdPlaceGame = Game(team_one=semiFinalGameOne.loser, team_two=semiFinalGameTwo.loser,
                          tournament=tournament,
                          game_type='3rd-Place Final', created_by=created_by)
    fifthPlaceGame = Game(team_one=loserSemiFinalGameOne.winner, team_two=loserSemiFinalGameTwo.winner,
                          tournament=tournament,
                          game_type='5th-Place Final', created_by=created_by)
    seventhPlaceGame = Game(team_one=loserSemiFinalGameOne.loser, team_two=loserSemiFinalGameTwo.loser,
                            tournament=tournament,
                            game_type='7th-Place Final', created_by=created_by)
    championshipGame.save()
    thirdPlaceGame.save()
    fifthPlaceGame.save()
    seventhPlaceGame.save()
    games = [championshipGame, thirdPlaceGame, fifthPlaceGame, seventhPlaceGame]
    tournament.final_round_initialized = True
    tournament.final_round_games.set(games)
    tournament.save()
