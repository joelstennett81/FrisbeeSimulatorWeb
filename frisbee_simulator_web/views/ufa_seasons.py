from frisbee_simulator_web.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from frisbee_simulator_web.views.simulate_tournament_functions import *


def detail_game(request, pk):
    game = UFASeasonGame.objects.prefetch_related(
        Prefetch('ufa_game_points', queryset=UFAPoint.objects.order_by('id'))
    ).get(pk=pk)

    points_with_quarter = []
    quarter = 1

    for i, point in enumerate(game.ufa_game_points.all()):
        if i != 0 and point.team_one_score_post_point == 0 and point.team_two_score_post_point == 0:
            quarter += 1
            continue
        points_with_quarter.append((quarter, point))

    top_assists = UFAPlayerGameStat.objects.filter(game=game).order_by(F('assists').desc())[:3]
    top_goals = UFAPlayerGameStat.objects.filter(game=game).order_by(F('goals').desc())[:3]
    top_throwaways = UFAPlayerGameStat.objects.filter(game=game).order_by(F('throwaways').desc())[:3]
    top_throwing_yards = UFAPlayerGameStat.objects.filter(game=game).order_by(F('throwing_yards').desc())[:3]
    top_receiving_yards = UFAPlayerGameStat.objects.filter(game=game).order_by(F('receiving_yards').desc())[:3]

    # Attach team to top player stats
    for stat_list in [top_assists, top_goals, top_throwaways, top_throwing_yards, top_receiving_yards]:
        for stat in stat_list:
            stat.team = stat.player.players_teams.filter(year=2025).first()

    # Team stats aggregation
    def get_team_totals(team):
        return UFAPlayerGameStat.objects.filter(game=game, player__ufa_player__teams=team).aggregate(
            total_assists=Sum('assists'),
            total_goals=Sum('goals'),
            total_throwing_yards=Sum('throwing_yards'),
            total_receiving_yards=Sum('receiving_yards'),
            total_throwaways=Sum('throwaways'),
            total_drops=Sum('drops'),
            total_blocks=Sum('turnovers_forced'),
        )

    team_one = game.team_one.team.ufa_team
    team_two = game.team_two.team.ufa_team
    team_one_totals = get_team_totals(team_one)
    team_two_totals = get_team_totals(team_two)

    return render(request, 'ufa_games/detail_game.html', {
        'game': game,
        'top_assists': top_assists,
        'top_goals': top_goals,
        'top_throwaways': top_throwaways,
        'top_throwing_yards': top_throwing_yards,
        'top_receiving_yards': top_receiving_yards,
        'team_one_totals': team_one_totals,
        'team_two_totals': team_two_totals,
        'team_one': team_one,
        'team_two': team_two,
        'points_with_quarter': points_with_quarter
    })


@login_required(login_url='/login/')
def detail_point(request, pk):
    point = get_object_or_404(UFAPoint, pk=pk)
    return render(request, 'ufa_games/detail_point.html', {'point': point})
