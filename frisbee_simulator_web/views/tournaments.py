from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView
from frisbee_simulator_web.models import Point
from frisbee_simulator_web.forms import TournamentForm
from frisbee_simulator_web.views.simulate_tournament_functions import *
from frisbee_simulator_web.views.teams import create_random_team
from frisbee_simulator_web.views.four_team_tournaments import *
from frisbee_simulator_web.views.eight_team_tournaments import *
from frisbee_simulator_web.views.sixteen_team_tournaments import *
from frisbee_simulator_web.views.twenty_team_tournaments import *


class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/create_tournament.html'
    success_url = '/tournaments/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_public = form.cleaned_data['is_public']
        self.object.created_by = self.request.user.profile

        # Check if teams were selected in the form
        teams = form.cleaned_data['teams']
        number_of_selected_teams = len(teams)
        if number_of_selected_teams > form.cleaned_data['number_of_teams']:
            # If too many teams are selected, add a message and redirect back to the form
            messages.error(self.request, 'You cannot select more than the designated number of teams')
            return self.form_invalid(form)
        # Subtract the number of selected teams from the total number of teams required for the tournament
        number_of_teams_to_create = int(form.cleaned_data['number_of_teams']) - number_of_selected_teams

        # Create the required number of random teams
        for _ in range(number_of_teams_to_create):
            team = create_random_team(self.request)
            team.is_public = form.cleaned_data['is_public']
            self.object.teams.add(team)

        # Add the selected teams to the tournament
        for team in teams:
            self.object.teams.add(team)

        self.object.save()
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class TournamentDeleteView(DeleteView):
    model = Tournament
    success_url = '/tournaments/'
    template_name = 'tournaments/tournament_confirm_delete.html'  # Replace with your template name


@login_required(login_url='/login/')
def list_tournaments(request, is_public=None):
    if is_public is None:
        tournaments = Tournament.objects.filter(created_by=request.user.profile)
    elif is_public:
        tournaments = Tournament.objects.filter(is_public=True).order_by('created_by')
    else:
        tournaments = Tournament.objects.filter(created_by=request.user.profile)
    return render(request, 'tournaments/list_tournaments.html', {'tournaments': tournaments})


def simulate_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if not tournament.pool_play_completed and not tournament.bracket_play_completed:
        return redirect(reverse('pool_play_overview', kwargs={'tournament_id': tournament_id}))
    elif tournament.pool_play_completed and not tournament.bracket_play_completed:
        return redirect(reverse('bracket_overview', kwargs={'tournament_id': tournament_id}))
    return redirect(reverse('tournament_results', kwargs={'tournament_id': tournament_id}))


def pool_play_overview(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if not tournament.pool_play_seeds_set:
        automatically_rank_teams_for_pool_play(request, tournament_id)
        return redirect('manually_rank_teams_for_pool_play', tournament_id=tournament.id)
    if not tournament.pool_play_initialized:
        setup_manual_pool_play_games_for_simulation(request, tournament_id)
    if tournament.number_of_teams == 4:
        tournament.pool_play_total_number_of_games = 6
        tournament.save()
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        return render(request, 'pool_play/four_team_pool_play_overview.html',
                      {'pool_a_games': pool_a_games, 'tournament': tournament,
                       'total_number_of_games': tournament.pool_play_total_number_of_games})
    elif tournament.number_of_teams == 8:
        tournament.pool_play_total_number_of_games = 12
        tournament.save()
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
        return render(request, 'pool_play/eight_team_pool_play_overview.html',
                      {'pool_a_games': pool_a_games, 'pool_b_games': pool_b_games, 'tournament': tournament,
                       'total_number_of_games': tournament.pool_play_total_number_of_games})
    elif tournament.number_of_teams == 16:
        tournament.pool_play_total_number_of_games = 24
        tournament.save()
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
        pool_c_games = tournament.pool_play_games.filter(pool__name='Pool C')
        pool_d_games = tournament.pool_play_games.filter(pool__name='Pool D')
        return render(request, 'pool_play/sixteen_team_pool_play_overview.html',
                      {'pool_a_games': pool_a_games, 'pool_b_games': pool_b_games, 'pool_c_games': pool_c_games,
                       'pool_d_games': pool_d_games, 'tournament': tournament,
                       'total_number_of_games': tournament.pool_play_total_number_of_games})
    elif tournament.number_of_teams == 20:
        tournament.pool_play_total_number_of_games = 40
        tournament.save()
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
        pool_c_games = tournament.pool_play_games.filter(pool__name='Pool C')
        pool_d_games = tournament.pool_play_games.filter(pool__name='Pool D')
        return render(request, 'pool_play/sixteen_team_pool_play_overview.html',
                      {'pool_a_games': pool_a_games, 'pool_b_games': pool_b_games, 'pool_c_games': pool_c_games,
                       'pool_d_games': pool_d_games, 'tournament': tournament,
                       'total_number_of_games': tournament.pool_play_total_number_of_games})
    else:
        total_number_of_games = 0
    return render(request, 'pool_play/pool_play_overview.html',
                  {'pool_play_games': tournament.pool_play_games, 'tournament': tournament,
                   'total_number_of_games': total_number_of_games})


def bracket_overview(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.number_of_teams == 4:
        if not tournament.semifinal_round_initialized:
            setup_semifinal_round_for_four_team_bracket(request, tournament_id)
            return render(request, 'bracket/four_team_bracket_overview.html', {'tournament': tournament})
        elif tournament.semifinal_round_initialized and not tournament.final_round_initialized:
            setup_final_round_for_four_team_bracket(request, tournament_id)
            return render(request, 'bracket/four_team_bracket_overview.html', {'tournament': tournament})
        else:
            return render(request, 'bracket/four_team_bracket_overview.html', {'tournament': tournament})
    elif tournament.number_of_teams == 8:
        if not tournament.quarterfinal_round_initialized:
            setup_quarterfinal_round_for_8_team_bracket(request, tournament_id)
        elif tournament.quarterfinal_round_initialized and not tournament.semifinal_round_initialized:
            setup_semifinal_round_for_eight_team_bracket(request, tournament_id)
            return render(request, 'bracket/eight_team_bracket_overview.html', {'tournament': tournament})
        elif tournament.quarterfinal_round_initialized and tournament.semifinal_round_initialized and not tournament.final_round_initialized:
            setup_final_round_for_eight_team_bracket(request, tournament_id)
            return render(request, 'bracket/eight_team_bracket_overview.html', {'tournament': tournament})
        else:
            return render(request, 'bracket/eight_team_bracket_overview.html', {'tournament': tournament})
        return render(request, 'bracket/eight_team_bracket_overview.html', {'tournament': tournament})
    elif tournament.number_of_teams == 16:
        if not tournament.pre_quarterfinal_round_initialized:
            setup_prequarterfinal_round_for_sixteen_team_bracket(request, tournament_id)
        elif tournament.pre_quarterfinal_round_initialized and not tournament.quarterfinal_round_initialized:
            setup_quarterfinal_round_for_sixteen_team_bracket(request, tournament_id)
        elif tournament.quarterfinal_round_initialized and not tournament.semifinal_round_initialized:
            setup_semifinal_round_for_sixteen_team_bracket(request, tournament_id)
            return render(request, 'bracket/sixteen_team_bracket_overview.html', {'tournament': tournament})
        elif tournament.quarterfinal_round_initialized and tournament.semifinal_round_initialized and not tournament.final_round_initialized:
            setup_final_round_for_sixteen_team_bracket(request, tournament_id)
            return render(request, 'bracket/sixteen_team_bracket_overview.html', {'tournament': tournament})
        else:
            return render(request, 'bracket/sixteen_team_bracket_overview.html', {'tournament': tournament})
        return render(request, 'bracket/sixteen_team_bracket_overview.html', {'tournament': tournament})
    elif tournament.number_of_teams == 20:
        if not tournament.pre_quarterfinal_round_initialized:
            setup_prequarterfinal_round_for_twenty_team_bracket(request, tournament_id)
        elif tournament.pre_quarterfinal_round_initialized and not tournament.quarterfinal_round_initialized:
            setup_quarterfinal_round_for_twenty_team_bracket(request, tournament_id)
        elif tournament.quarterfinal_round_initialized and not tournament.semifinal_round_initialized:
            setup_semifinal_round_for_twenty_team_bracket(request, tournament_id)
            return render(request, 'bracket/twenty_team_bracket_overview.html', {'tournament': tournament})
        elif tournament.quarterfinal_round_initialized and tournament.semifinal_round_initialized and not tournament.final_round_initialized:
            setup_final_round_for_twenty_team_bracket(request, tournament_id)
            return render(request, 'bracket/twenty_team_bracket_overview.html', {'tournament': tournament})
        else:
            return render(request, 'bracket/twenty_team_bracket_overview.html', {'tournament': tournament})
        return render(request, 'bracket/twenty_team_bracket_overview.html', {'tournament': tournament})


def simulate_game(request, game_id, tournament_id):
    game = Game.objects.get(id=game_id)
    tournament = Tournament.objects.get(id=tournament_id)
    gameSimulation = GameSimulation(tournament, game)
    gameSimulation.coin_flip()
    gameSimulation.simulationType = game.tournament.simulation_type
    gameSimulation.simulate_full_game()
    if gameSimulation.winner == gameSimulation.teamInGameSimulationOne:
        game.winner = gameSimulation.teamInGameSimulationOne.tournamentTeam
        game.loser = gameSimulation.teamInGameSimulationTwo.tournamentTeam
        point_differential = abs(
            gameSimulation.teamInGameSimulationOne.score - gameSimulation.teamInGameSimulationTwo.score)
    else:
        game.winner = gameSimulation.teamInGameSimulationTwo.tournamentTeam
        game.loser = gameSimulation.teamInGameSimulationOne.tournamentTeam
        point_differential = abs(
            gameSimulation.teamInGameSimulationTwo.score - gameSimulation.teamInGameSimulationOne.score)
    if game.game_type == 'Pool Play':
        TournamentTeam.objects.filter(pk=game.winner.pk).update(pool_play_wins=F('pool_play_wins') + 1,
                                                                pool_play_point_differential=F(
                                                                    'pool_play_point_differential') + point_differential)
        TournamentTeam.objects.filter(pk=game.loser.pk).update(pool_play_losses=F('pool_play_losses') + 1,
                                                               pool_play_point_differential=F(
                                                                   'pool_play_point_differential') - point_differential)
        tournament.pool_play_games_completed_counter += 1
        tournament.save()
        if tournament.pool_play_games_completed_counter == tournament.pool_play_total_number_of_games:
            tournament.pool_play_completed = True
            tournament.save()
    else:
        game.winner.bracket_play_wins += 1
        game.loser.bracket_play_losses += 1
    game.created_by = request.user.profile
    game.is_completed = True
    game.save()
    if game.game_type == 'Pool Play':
        return redirect(reverse('pool_play_overview', kwargs={'tournament_id': tournament_id}))
    elif game.game_type in ['Pre-Quarterfinal', 'Quarterfinal', 'Loser-Semifinal', 'Fifth-Place Final',
                            'Seventh-Place Final', 'Semifinal', 'Championship', '9th-Place Quarterfinal',
                            '13th-Place Semifinal', '15th-Place Final',
                            '9th-Place Semifinal', '11th-Place Final', '9th-Place Final', '13th-Place Semifinal',
                            '15th-Place Final', '17th-Place Semifinal', '19th-Place Final']:
        return redirect(reverse('bracket_overview', kwargs={'tournament_id': tournament_id}))
    else:
        return redirect(reverse('list_tournaments'))


def check_pool_play_simulation_status(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.pool_play_completed:
        completed = True
    else:
        completed = False
    return JsonResponse({'simulations_complete': completed})


def check_bracket_simulation_status(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    incomplete_games = Game.objects.filter(tournament=tournament, is_completed=False)
    return JsonResponse({'simulations_complete': not incomplete_games.exists()})


def fetch_latest_games_data(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    games = Game.objects.filter(tournament=tournament)
    game_data = []
    for game in games:
        winner_team_name = game.winner.team.location + ' ' + game.winner.team.mascot if game.winner else None
        loser_team_name = game.loser.team.location + ' ' + game.loser.team.mascot if game.loser else None
        game_dict = {
            'id': game.id,
            'is_completed': game.is_completed,
            'winner_team': winner_team_name,
            'loser_team': loser_team_name,
            'winner_score': game.winner_score,
            'loser_score': game.loser_score,
            'tournament_id': tournament_id
        }
        game_data.append(game_dict)
    return JsonResponse({'games': game_data})


def simulate_full_pool_play(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    for game in tournament.pool_play_games.all():
        if not game.is_completed:
            simulate_game(request, game.id, tournament.id)
    tournament.pool_play_completed = True
    tournament.save()
    return redirect(reverse('pool_play_results', kwargs={'tournament_id': tournament_id}))


def simulate_prequarterfinal_round(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    for game in tournament.pre_quarterfinal_round_games.all():
        if not game.is_completed:
            simulate_game(request, game.id, tournament.id)
    tournament.pre_quarterfinal_round_completed = True
    tournament.save()
    return redirect(reverse('bracket_overview', kwargs={'tournament_id': tournament_id}))


def simulate_quarterfinal_round(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    for game in tournament.quarterfinal_round_games.all():
        if not game.is_completed:
            simulate_game(request, game.id, tournament.id)
    tournament.quarterfinal_round_completed = True
    if tournament.number_of_teams == 16:
        for game in tournament.losers_quarterfinal_round_games.all():
            if not game.is_completed:
                simulate_game(request, game.id, tournament.id)
        tournament.losers_quarterfinal_round_completed = True
    tournament.save()
    return redirect(reverse('bracket_overview', kwargs={'tournament_id': tournament_id}))


def simulate_semifinal_round(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    for game in tournament.semifinal_round_games.all():
        if not game.is_completed:
            simulate_game(request, game.id, tournament.id)
    tournament.semifinal_round_completed = True
    if tournament.number_of_teams == 16:
        for game in tournament.losers_semifinal_round_games.all():
            if not game.is_completed:
                simulate_game(request, game.id, tournament.id)
        tournament.losers_semifinal_round_completed = True
    tournament.save()
    return redirect(reverse('bracket_overview', kwargs={'tournament_id': tournament_id}))


def simulate_final_round(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    for game in tournament.final_round_games.all():
        if not game.is_completed:
            simulate_game(request, game.id, tournament.id)
    if tournament.number_of_teams == 16:
        for game in tournament.losers_final_round_games.all():
            if not game.is_completed:
                simulate_game(request, game.id, tournament.id)
        tournament.losers_final_round_completed = True
    championship_game = Game.objects.get(tournament=tournament, game_type='Championship')
    tournament.champion = championship_game.winner.team
    tournament.final_round_completed = True
    tournament.save()
    tournament.is_complete = True
    tournament.bracket_play_completed = True
    tournament.save()
    save_tournament_player_stats_from_game_player_stats(tournament_id)
    return redirect(reverse('tournament_results', kwargs={'tournament_id': tournament_id}))


def save_tournament_player_stats_from_game_player_stats(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournamentTeams = TournamentTeam.objects.filter(tournament_id=tournament_id)
    for tournamentTeam in tournamentTeams:
        team = tournamentTeam.team
        teamPlayers = team.players.all()
        for player in teamPlayers:
            gameStats = PlayerGameStat.objects.filter(player=player,
                                                      game__game_type='Pool Play',
                                                      tournament=tournament)
            playerTournamentStat, created = PlayerTournamentStat.objects.get_or_create(
                tournament=tournament,
                player=player,
                team=team
            )
            aggregates = gameStats.aggregate(
                goals=Sum('goals'),
                assists=Sum('assists'),
                swing_passes_thrown=Sum('swing_passes_thrown'),
                swing_passes_completed=Sum('swing_passes_completed'),
                under_passes_thrown=Sum('under_passes_thrown'),
                under_passes_completed=Sum('under_passes_completed'),
                short_hucks_thrown=Sum('short_hucks_thrown'),
                short_hucks_completed=Sum('short_hucks_completed'),
                deep_hucks_thrown=Sum('deep_hucks_thrown'),
                deep_hucks_completed=Sum('deep_hucks_completed'),
                throwing_yards=Sum('throwing_yards'),
                receiving_yards=Sum('receiving_yards'),
                turnovers_forced=Sum('turnovers_forced'),
                throwaways=Sum('throwaways'),
                drops=Sum('drops'),
                callahans=Sum('callahans'),
                pulls=Sum('pulls')
            )
            for attr, value in aggregates.items():
                if value is not None:
                    setattr(playerTournamentStat, attr, value)
            playerTournamentStat.save()


@login_required(login_url='/login/')
def game_results(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return JsonResponse(game)


@login_required(login_url='/login/')
def pool_play_results(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    number_of_teams = tournament.number_of_teams
    teams = TournamentTeam.objects.filter(tournament=tournament).order_by('-pool_play_wins',
                                                                          '-pool_play_point_differential')
    teams_stats = []
    for team in teams:
        team_stats = {
            'team': team,
            'pool_play_wins': team.pool_play_wins,
            'pool_play_losses': team.pool_play_losses,
            'pool_play_point_differential': team.pool_play_point_differential
        }
        teams_stats.append(team_stats)
    top_assists = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('assists').desc())[:3]
    top_goals = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('goals').desc())[:3]
    top_throwaways = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('throwaways').desc())[:3]
    top_throwing_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('throwing_yards').desc())[:3]
    top_receiving_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('receiving_yards').desc())[:3]
    if number_of_teams == 4:
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
        pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        context = {'tournament': tournament, 'teams_stats': teams_stats, 'top_assists': top_assists,
                   'top_goals': top_goals,
                   'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                   'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                   'pool_a_teams': pool_a_teams}
        return render(request, 'pool_play/four_team_pool_play_results.html', context)
    elif number_of_teams == 8:
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
        pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
        pool_b = TournamentPool.objects.get(tournament=tournament, name='Pool B')
        pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        pool_b_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_b).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        context = {'tournament': tournament, 'teams_stats': teams_stats, 'top_assists': top_assists,
                   'top_goals': top_goals,
                   'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                   'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                   'pool_b_games': pool_b_games, 'pool_a_teams': pool_a_teams, 'pool_b_teams': pool_b_teams}
        return render(request, 'pool_play/eight_team_pool_play_results.html', context)
    elif number_of_teams == 16:
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
        pool_c_games = tournament.pool_play_games.filter(pool__name='Pool C')
        pool_d_games = tournament.pool_play_games.filter(pool__name='Pool D')
        pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
        pool_b = TournamentPool.objects.get(tournament=tournament, name='Pool B')
        pool_c = TournamentPool.objects.get(tournament=tournament, name='Pool C')
        pool_d = TournamentPool.objects.get(tournament=tournament, name='Pool D')
        pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        pool_b_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_b).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        pool_c_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_c).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        pool_d_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_d).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        context = {'tournament': tournament, 'teams_stats': teams_stats, 'top_assists': top_assists,
                   'top_goals': top_goals,
                   'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                   'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                   'pool_b_games': pool_b_games, 'pool_c_games': pool_c_games,
                   'pool_d_games': pool_d_games, 'pool_a_teams': pool_a_teams, 'pool_b_teams': pool_b_teams,
                   'pool_c_teams': pool_c_teams, 'pool_d_teams': pool_d_teams}
        return render(request, 'pool_play/sixteen_team_pool_play_results.html', context)
    elif number_of_teams == 20:
        pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
        pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
        pool_c_games = tournament.pool_play_games.filter(pool__name='Pool C')
        pool_d_games = tournament.pool_play_games.filter(pool__name='Pool D')
        pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
        pool_b = TournamentPool.objects.get(tournament=tournament, name='Pool B')
        pool_c = TournamentPool.objects.get(tournament=tournament, name='Pool C')
        pool_d = TournamentPool.objects.get(tournament=tournament, name='Pool D')
        pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        pool_b_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_b).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        pool_c_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_c).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        pool_d_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_d).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
        context = {'tournament': tournament, 'teams_stats': teams_stats, 'top_assists': top_assists,
                   'top_goals': top_goals,
                   'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                   'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                   'pool_b_games': pool_b_games, 'pool_c_games': pool_c_games,
                   'pool_d_games': pool_d_games, 'pool_a_teams': pool_a_teams, 'pool_b_teams': pool_b_teams,
                   'pool_c_teams': pool_c_teams, 'pool_d_teams': pool_d_teams}
        return render(request, 'pool_play/twenty_team_pool_play_results.html', context)


@login_required(login_url='/login/')
def tournament_results(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    number_of_teams = tournament.number_of_teams
    teams = TournamentTeam.objects.filter(tournament=tournament)
    teams_stats = []
    for team in teams:
        team_stats = {
            'team': team,
            'pool_play_wins': team.pool_play_wins,
            'pool_play_losses': team.pool_play_losses,
            'pool_play_point_differential': team.pool_play_point_differential
        }
        teams_stats.append(team_stats)
    top_assists = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('assists').desc())[:3]
    top_goals = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('goals').desc())[:3]
    top_throwaways = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('throwaways').desc())[:3]
    top_throwing_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('throwing_yards').desc())[:3]
    top_receiving_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('receiving_yards').desc())[:3]
    if tournament.pool_play_completed and not tournament.semifinal_round_completed and not tournament.final_round_completed:
        return redirect(reverse('pool_play_results', kwargs={'tournament_id': tournament_id}))
    elif tournament.pool_play_completed and tournament.semifinal_round_completed and tournament.final_round_completed:
        if number_of_teams == 4:
            pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
            pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
            pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            context = {'tournament_id': tournament_id, 'tournament': tournament, 'teams_stats': teams_stats,
                       'top_assists': top_assists, 'top_goals': top_goals, 'top_throwaways': top_throwaways,
                       'top_throwing_yards': top_throwing_yards,
                       'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                       'pool_a_teams': pool_a_teams}
            return render(request, 'tournaments/four_team_tournament_results.html', context)
        elif number_of_teams == 8:
            pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
            pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
            pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
            pool_b = TournamentPool.objects.get(tournament=tournament, name='Pool B')
            pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_b_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_b).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            context = {'tournament_id': tournament_id, 'tournament': tournament, 'teams_stats': teams_stats,
                       'top_assists': top_assists,
                       'top_goals': top_goals,
                       'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                       'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                       'pool_b_games': pool_b_games, 'pool_a_teams': pool_a_teams, 'pool_b_teams': pool_b_teams}
            return render(request, 'tournaments/eight_team_tournament_results.html', context)
        elif number_of_teams == 16:
            pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A')
            pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B')
            pool_c_games = tournament.pool_play_games.filter(pool__name='Pool C')
            pool_d_games = tournament.pool_play_games.filter(pool__name='Pool D')
            pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
            pool_b = TournamentPool.objects.get(tournament=tournament, name='Pool B')
            pool_c = TournamentPool.objects.get(tournament=tournament, name='Pool C')
            pool_d = TournamentPool.objects.get(tournament=tournament, name='Pool D')
            pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_b_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_b).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_c_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_c).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_d_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_d).order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            context = {'tournament_id': tournament_id, 'tournament': tournament, 'teams_stats': teams_stats,
                       'top_assists': top_assists,
                       'top_goals': top_goals,
                       'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                       'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                       'pool_b_games': pool_b_games, 'pool_c_games': pool_c_games,
                       'pool_d_games': pool_d_games, 'pool_a_teams': pool_a_teams, 'pool_b_teams': pool_b_teams,
                       'pool_c_teams': pool_c_teams, 'pool_d_teams': pool_d_teams}
            return render(request, 'tournaments/sixteen_team_tournament_results.html', context)
        elif number_of_teams == 20:
            pool_a_games = tournament.pool_play_games.filter(pool__name='Pool A').order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_b_games = tournament.pool_play_games.filter(pool__name='Pool B').order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_c_games = tournament.pool_play_games.filter(pool__name='Pool C').order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_d_games = tournament.pool_play_games.filter(pool__name='Pool D').order_by('-pool_play_wins',
                                                                                                  '-pool_play_point_differential')
            pool_a = TournamentPool.objects.get(tournament=tournament, name='Pool A')
            pool_b = TournamentPool.objects.get(tournament=tournament, name='Pool B')
            pool_c = TournamentPool.objects.get(tournament=tournament, name='Pool C')
            pool_d = TournamentPool.objects.get(tournament=tournament, name='Pool D')
            pool_a_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_a)
            pool_b_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_b)
            pool_c_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_c)
            pool_d_teams = TournamentTeam.objects.filter(tournament=tournament, pool=pool_d)
            context = {'tournament_id': tournament_id, 'tournament': tournament, 'teams_stats': teams_stats,
                       'top_assists': top_assists,
                       'top_goals': top_goals,
                       'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                       'top_receiving_yards': top_receiving_yards, 'pool_a_games': pool_a_games,
                       'pool_b_games': pool_b_games, 'pool_c_games': pool_c_games,
                       'pool_d_games': pool_d_games, 'pool_a_teams': pool_a_teams, 'pool_b_teams': pool_b_teams,
                       'pool_c_teams': pool_c_teams, 'pool_d_teams': pool_d_teams}
            return render(request, 'tournaments/twenty_team_tournament_results.html', context)
        else:
            return render(request, 'tournaments/tournament_error.html')
    else:
        return render(request, 'tournaments/tournament_error.html')


def get_context_for_tournament_results(tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    teams = TournamentTeam.objects.filter(tournament=tournament)
    teams_stats = []
    for team in teams:
        team_stats = {
            'team': team,
            'pool_play_wins': team.pool_play_wins,
            'pool_play_losses': team.pool_play_losses,
            'pool_play_point_differential': team.pool_play_point_differential
        }
        teams_stats.append(team_stats)

    top_assists = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('assists').desc())[:3]
    top_goals = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('goals').desc())[:3]
    top_throwaways = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('throwaways').desc())[:3]
    top_throwing_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('throwing_yards').desc())[:3]
    top_receiving_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('receiving_yards').desc())[:3]

    context = {'tournament': tournament, 'teams_stats': teams_stats, 'top_assists': top_assists,
               'top_goals': top_goals,
               'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
               'top_receiving_yards': top_receiving_yards}
    return context


@login_required(login_url='/login/')
def four_team_tournament_results(request, tournament_id):
    context = get_context_for_tournament_results(tournament_id)
    return render(request, 'tournaments/four_team_tournament_results.html', context)


@login_required(login_url='/login/')
def eight_team_tournament_results(request, tournament_id):
    context = get_context_for_tournament_results(tournament_id)
    return render(request, 'tournaments/eight_team_tournament_results.html', context)


@login_required(login_url='/login/')
def sixteen_team_tournament_results(request, tournament_id):
    context = get_context_for_tournament_results(tournament_id)
    return render(request, 'tournaments/sixteen_team_tournament_results.html', context)


@login_required(login_url='/login/')
def detail_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    return render(request, 'tournaments/detail_tournament.html', {'tournament': tournament})


@login_required(login_url='/login/')
def detail_game(request, pk):
    game = Game.objects.prefetch_related(Prefetch('game_points', queryset=Point.objects.order_by('id'))).get(pk=pk)
    return render(request, 'tournaments/detail_game.html', {'game': game})


@login_required(login_url='/login/')
def detail_point(request, pk):
    point = get_object_or_404(Point, pk=pk)
    return render(request, 'tournaments/detail_point.html', {'point': point})
