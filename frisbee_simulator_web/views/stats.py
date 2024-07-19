from django.shortcuts import render

from frisbee_simulator_web.models import Tournament, PlayerTournamentStat, Player, PlayerGameStat, Game


def list_player_tournament_stats(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    playerTournamentStats = PlayerTournamentStat.objects.filter(tournament=tournament)
    return render(request,
                  'stats/player_tournament_stats/list_player_tournament_stats.html',
                  {'playerTournamentStats': playerTournamentStats})


def detail_player_tournament_stats(request, tournament_id, player_id):
    tournament = Tournament.objects.get(id=tournament_id)
    player = Player.objects.get(id=player_id)
    playerTournamentStat = PlayerTournamentStat.objects.get(tournament=tournament, player=player)
    return render(request,
                  'stats/player_tournament_stats/detail_player_tournament_stats.html',
                  {'playerTournamentStat': playerTournamentStat})
