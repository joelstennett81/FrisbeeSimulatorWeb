from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from frisbee_simulator_web.forms import TeamForm
from frisbee_simulator_web.models import Team
from frisbee_simulator_web.views.misc import create_random_player, generate_random_city, generate_random_mascot, \
    calculate_overall_team_rating


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/create_team.html'
    success_url = '/teams/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
def random_team(request):
    team = create_random_team(request)
    team.save()
    return redirect('list_teams')


def create_random_team(request):
    team = Team(
        location=generate_random_city(50),
        mascot=generate_random_mascot()
    )
    team.save()
    o_line_handles = [create_random_player(request, "OFFENSE", "HANDLE") for _ in range(3)]
    o_line_cutters = [create_random_player(request, "OFFENSE", "CUTTER") for _ in range(4)]
    d_line_handles = [create_random_player(request, "DEFENSE", "HANDLE") for _ in range(3)]
    d_line_cutters = [create_random_player(request, "DEFENSE", "CUTTER") for _ in range(4)]
    bench_handles = [create_random_player(request, "BENCH", "HANDLE") for _ in range(3)]
    bench_cutters = [create_random_player(request, "BENCH", "CUTTER") for _ in range(4)]
    o_line_players = o_line_handles + o_line_cutters
    d_line_players = d_line_handles + d_line_cutters
    bench_players = bench_handles + bench_cutters
    players = o_line_players + d_line_players + bench_players
    for player in players:
        player.is_public = team.is_public
    team.players.set(players)
    team.o_line_players.set(o_line_players)
    team.d_line_players.set(d_line_players)
    team.bench_players.set(bench_players)
    team.created_by = request.user.profile
    team.save()
    team.overall_rating = calculate_overall_team_rating(team)
    team.save()
    return team


@login_required(login_url='/login/')
def list_teams(request, is_public=None):
    if is_public is None:
        teams = Team.objects.filter(created_by=request.user.profile)
    elif is_public:
        teams = Team.objects.filter(is_public=True).order_by('created_by')
    else:
        teams = Team.objects.filter(created_by=request.user.profile)
    return render(request, 'teams/list_teams.html', {'teams': teams})


@login_required(login_url='/login/')
def detail_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/detail_team.html', {'team': team})


class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/edit_team.html'  # Assuming you have a template named 'edit_team.html'
    success_url = '/teams/'  # Redirect to the list of teams after successful update

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # Custom logic to handle form submission
        team = form.save(commit=False)
        team.created_by = self.request.user.profile
        team.save()
        form.save_m2m()  # Save many-to-many fields
        return super().form_valid(form)
