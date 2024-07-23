from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
import os
from django.shortcuts import render, redirect
from django.views.static import serve
from tablib import Dataset
from app import settings
from frisbee_simulator_web.forms import PlayerForm, UploadFileForm
from frisbee_simulator_web.models import Player
from frisbee_simulator_web.resources import PlayerResource
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


def upload_players_spreadsheet(request):
    if request.method == 'POST':
        player_resource = PlayerResource()
        dataset = Dataset().load(request.FILES['file'].read(), format='xlsx')
        result = player_resource.import_data(dataset,
                                             dry_run=False)  # Set dry_run=True to test the import without saving

        if not result.has_errors():
            return redirect('list_players')  # Redirect to success page after successful import
    else:
        form = UploadFileForm()  # Assuming you have an UploadFileForm defined
    return render(request, 'players/upload_player_spreadsheet.html', {'form': form})  # Render form on GET request

