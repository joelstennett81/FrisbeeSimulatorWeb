import random
import threading
from itertools import chain, count

from django.contrib import messages
from django.db.models import Sum, F, Prefetch
from django.shortcuts import render, redirect

from frisbee_simulator_web.models import PlayerTournamentStat, TournamentTeam, TournamentPool, Game, TournamentBracket, \
    PlayerGameStat, Tournament
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation


def setup_manual_pool_play_games_for_simulation(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_teams = list(TournamentTeam.objects.filter(tournament=tournament))
    num_teams = len(tournament_teams)
    games = []
    # Check the number of teams and create games accordingly
    if num_teams == 4:
        pool = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(tournament_teams),
                                             name='Pool A')
        pool.teams.set(tournament_teams)
        for team in tournament_teams:
            team.pool = pool
            team.save()
        pool.save()
        # Round  1
        games.extend([
            Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[1],
                                tournament=tournament, game_type='Pool Play'),
            Game.objects.create(team_one=tournament_teams[2], team_two=tournament_teams[3],
                                tournament=tournament, game_type='Pool Play')
        ])
        # Round  2
        games.extend([
            Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[2],
                                tournament=tournament, game_type='Pool Play'),
            Game.objects.create(team_one=tournament_teams[1], team_two=tournament_teams[3],
                                tournament=tournament, game_type='Pool Play')
        ])
        # Round  3
        games.extend([
            Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[3],
                                tournament=tournament, game_type='Pool Play'),
            Game.objects.create(team_one=tournament_teams[1], team_two=tournament_teams[2],
                                tournament=tournament, game_type='Pool Play')
        ])
    elif num_teams == 8:
        poolATeams = [tournament_teams[i] for i in [0, 3, 4, 7]]
        poolBTeams = [tournament_teams[i] for i in [1, 2, 5, 6]]
        poolA = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolATeams),
                                              name='Pool A')
        poolB = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolBTeams),
                                              name='Pool B')
        poolA.teams.set(poolATeams)
        for team in poolATeams:
            team.pool = poolA
            team.save()
        poolA.save()
        poolB.teams.set(poolBTeams)
        for team in poolBTeams:
            team.pool = poolB
            team.save()
        poolB.save()
        # Pool A games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  2
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  3
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA)
        ])
        # Pool B games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  2
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  3
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB)
        ])
    elif num_teams == 16:
        poolATeams = [tournament_teams[0], tournament_teams[7], tournament_teams[11], tournament_teams[12]]
        poolBTeams = [tournament_teams[1], tournament_teams[6], tournament_teams[10], tournament_teams[13]]
        poolCTeams = [tournament_teams[2], tournament_teams[5], tournament_teams[9], tournament_teams[14]]
        poolDTeams = [tournament_teams[3], tournament_teams[4], tournament_teams[8], tournament_teams[15]]
        poolA = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolATeams),
                                              name='Pool A')
        poolB = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolBTeams),
                                              name='Pool B')
        poolC = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolCTeams),
                                              name='Pool C')
        poolD = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolDTeams),
                                              name='Pool D')
        poolA.teams.set(poolATeams)
        poolA.save()
        poolB.teams.set(poolBTeams)
        poolB.save()
        poolC.teams.set(poolCTeams)
        poolC.save()
        poolD.teams.set(poolDTeams)
        poolD.save()
        for team in poolATeams:
            team.pool = poolA
            team.save()
        for team in poolBTeams:
            team.pool = poolB
            team.save()
        for team in poolCTeams:
            team.pool = poolC
            team.save()
        for team in poolDTeams:
            team.pool = poolD
            team.save()
        # Pool A games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  2
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  3
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA)
        ])
        # Pool B games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  2
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  3
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB)
        ])
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[2], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  2
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  3
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolC)
        ])
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[2], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  2
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  3
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolD)
        ])
    elif num_teams == 20:
        poolATeams = [tournament_teams[0], tournament_teams[7], tournament_teams[11], tournament_teams[12],
                      tournament_teams[16]]
        poolBTeams = [tournament_teams[1], tournament_teams[6], tournament_teams[10], tournament_teams[13],
                      tournament_teams[17]]
        poolCTeams = [tournament_teams[2], tournament_teams[5], tournament_teams[9], tournament_teams[14],
                      tournament_teams[18]]
        poolDTeams = [tournament_teams[3], tournament_teams[4], tournament_teams[8], tournament_teams[15],
                      tournament_teams[19]]
        poolA = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolATeams),
                                              name='Pool A')
        poolB = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolBTeams),
                                              name='Pool B')
        poolC = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolCTeams),
                                              name='Pool C')
        poolD = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolDTeams),
                                              name='Pool D')
        poolA.teams.set(poolATeams)
        poolA.save()
        poolB.teams.set(poolBTeams)
        poolB.save()
        poolC.teams.set(poolCTeams)
        poolC.save()
        poolD.teams.set(poolDTeams)
        poolD.save()
        for team in poolATeams:
            team.pool = poolA
            team.save()
        for team in poolBTeams:
            team.pool = poolB
            team.save()
        for team in poolCTeams:
            team.pool = poolC
            team.save()
        for team in poolDTeams:
            team.pool = poolD
            team.save()
        # Pool A games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  2
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[3], team_two=poolATeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  3
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  4
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  5
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
        ])
        # Pool B
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  2
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[3], team_two=poolBTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  3
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  4
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  5
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
        ])
        # Pool C
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[2], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  2
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[3], team_two=poolCTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  3
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  4
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  5
            Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[2], team_two=poolCTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
        ])

        # Pool D
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[2], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  2
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[3], team_two=poolDTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  3
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  4
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  5
            Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[2], team_two=poolDTeams[4], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
        ])

    tournament.pool_play_initialized = True
    tournament.pool_play_games.set(games)
    tournament.save()


def automatically_rank_teams_for_pool_play(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    teams = list(tournament.teams.all())
    teams.sort(key=lambda team: (-team.overall_rating, team.location))
    for i, team in enumerate(teams):
        pool_play_seed = i + 1
        tournament_team = TournamentTeam.objects.create(team=team, tournament=tournament,
                                                        pool_play_seed=pool_play_seed,
                                                        bracket_play_seed=pool_play_seed, pool_play_wins=0)
        tournament_team.save()
    tournament.save()


def manually_rank_teams_for_pool_play(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_teams = TournamentTeam.objects.filter(tournament=tournament)
    if request.method == 'POST':
        # Extract seeds from the POST data
        seeds = {key.split('-')[1]: int(value) for key, value in request.POST.items() if key.startswith('seed-')}

        # Check if all seeds are unique and within the valid range
        if len(seeds) != tournament.teams.count():
            messages.error(request, "Each team must have a unique seed.")
            return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                          {'tournament': tournament, 'teams': tournament_teams})
        if len(set(seeds.values())) != len(seeds):
            messages.error(request, "Seeds must be unique.")
            return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                          {'tournament': tournament, 'teams': tournament_teams})
        min_seed = 1
        max_seed = tournament.teams.count()
        if not all(min_seed <= seed <= max_seed for seed in seeds.values()):
            messages.error(request, f"Seeds must be between {min_seed} and {max_seed}.")
            return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                          {'tournament': tournament, 'teams': tournament_teams})

        # If validation passes, update the teams' seeds
        for team_id, seed in seeds.items():
            team = TournamentTeam.objects.get(id=team_id, tournament=tournament)
            team.seed = seed
            team.save()

        # Mark the seeds as set for the tournament
        tournament.pool_play_seeds_set = True
        tournament.save()

        # Redirect back to the pool play overview or another appropriate view
        return redirect('pool_play_overview', tournament_id=tournament.id)
    else:
        # Render the template for manual seed setting
        return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                      {'tournament': tournament, 'teams': tournament_teams})


def simulate_bracket_game(request, game, tournament):
    gameSimulation = GameSimulation(tournament, game)
    gameSimulation.coin_flip()
    gameSimulation.simulationType = game.tournament.simulation_type
    gameSimulation.simulate_full_game()
    # Determine the winner and loser
    if gameSimulation.winner == gameSimulation.tournamentTeamOne:
        game.winner = gameSimulation.tournamentTeamOne
        game.loser = gameSimulation.tournamentTeamTwo
    else:
        game.winner = gameSimulation.tournamentTeamTwo
        game.loser = gameSimulation.tournamentTeamOne
    # Increment the winner and loser's statistics
    game.winner.bracket_play_wins += 1
    game.loser.bracket_play_losses += 1
    game.save()
    game.created_by = request.user.profile
    game.save()
    return game
