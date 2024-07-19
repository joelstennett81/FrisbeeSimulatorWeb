from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from frisbee_simulator_web.forms import PlayerForm
from frisbee_simulator_web.models import Player
from frisbee_simulator_web.views.misc import create_random_player


class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'players/create_player.html'
    success_url = '/players/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


@login_required(login_url='/login/')
def list_players(request, is_public=None):
    if is_public is None:
        players = Player.objects.filter(created_by=request.user.profile)
    elif is_public:
        players = Player.objects.filter(is_public=True).order_by('created_by')
    else:
        players = Player.objects.filter(created_by=request.user.profile)
    return render(request, 'players/list_players.html', {'players': players})


@login_required(login_url='/login/')
def detail_player(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'players/detail_player.html', {'player': player})


class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'players/edit_player.html'
    success_url = reverse_lazy('list_players')  # Redirect to the list of players after update

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
