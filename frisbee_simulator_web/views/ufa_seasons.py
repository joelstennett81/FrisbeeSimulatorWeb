from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

# from frisbee_simulator_web.views.simulate_tournament_functions import *

from frisbee_simulator_web.models import *


@login_required(login_url='/login/')
def detail_game(request, pk):
    game = UFASeasonGame.objects.prefetch_related(Prefetch('ufa_game_points', queryset=UFAPoint.objects.order_by('id'))).get(pk=pk)

    return render(request, 'ufa_games/detail_game.html', {'game': game})


@login_required(login_url='/login/')
def detail_point(request, pk):
    point = get_object_or_404(UFAPoint, pk=pk)
    return render(request, 'ufa_games/detail_point.html', {'point': point})