from frisbee_simulator_web.models import Tournament, TournamentBracket, TournamentPool, Game


def setup_semifinal_round_for_four_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_pool = TournamentPool.objects.get(tournament=tournament)
    teams = tournament_pool.teams.all()
    sorted_teams = teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    tournament_bracket = TournamentBracket(tournament=tournament, number_of_teams=4,
                                           bracket_type='Championship')
    tournament_bracket.save()
    tournament_bracket.teams.set(sorted_teams)
    tournament_bracket.save()
    for i, team in enumerate(sorted_teams, start=1):
        team.bracket_play_seed = i
        team.save()
    teams_in_bracket = tournament_bracket.teams.all()
    created_by = request.user.profile
    game_one = Game(team_one=teams_in_bracket[0], team_two=teams_in_bracket[3],
                    tournament=tournament_bracket.tournament,
                    game_type='Semifinal', created_by=created_by)
    game_two = Game(team_one=teams_in_bracket[1], team_two=teams_in_bracket[2],
                    tournament=tournament_bracket.tournament,
                    game_type='Semifinal', created_by=created_by)
    game_one.save()
    game_two.save()
    games = [game_one, game_two]
    tournament.semifinal_round_initialized = True
    tournament.semifinal_round_games.set(games)
    tournament.save()


def setup_final_round_for_four_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    semifinalGames = tournament.semifinal_round_games.all()
    semifinalGameOne = semifinalGames[0]
    semifinalGameTwo = semifinalGames[1]
    created_by = request.user.profile
    third_place_game = Game(team_one=semifinalGameOne.loser, team_two=semifinalGameTwo.loser,
                            tournament=tournament,
                            game_type='3rd-Place Final', created_by=created_by)
    championship_game = Game(team_one=semifinalGameOne.winner, team_two=semifinalGameTwo.winner,
                             tournament=tournament,
                             game_type='Championship', created_by=created_by)
    third_place_game.save()
    championship_game.save()
    games = [third_place_game, championship_game]
    tournament.final_round_initialized = True
    tournament.final_round_games.set(games)
    tournament.save()