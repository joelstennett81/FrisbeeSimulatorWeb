from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import models
from django_select2.forms import Select2MultipleWidget

from .models import Player, Team, Tournament, Profile, Game, TournamentTeam
from .views.misc import calculate_overall_team_rating, calculate_overall_player_rating, calculate_handle_offense_rating, \
    calculate_handle_defense_rating, calculate_cutter_offense_rating, calculate_cutter_defense_rating, \
    create_random_player
from django.db.models import Q


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PlayerForm(forms.ModelForm):
    is_public = forms.BooleanField(
        required=False,
        help_text="Do you want to allow other users to see and use this?"
    )

    class Meta:
        model = Player
        exclude = ['teams', 'seasons', 'overall_rating', 'overall_handle_offense_rating',
                   'overall_handle_defense_rating', 'overall_cutter_offense_rating', 'overall_cutter_defense_rating',
                   'created_by']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        player = super().save(commit=False)
        player.overall_rating = calculate_overall_player_rating(player)
        player.overall_handle_offense_rating = calculate_handle_offense_rating(player)
        player.overall_handle_defense_rating = calculate_handle_defense_rating(player)
        player.overall_cutter_offense_rating = calculate_cutter_offense_rating(player)
        player.overall_cutter_defense_rating = calculate_cutter_defense_rating(player)
        player.created_by = self.request.user.profile
        if commit:
            player.save()
        return player


class TeamForm(forms.ModelForm):
    o_line_players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 10, 'style': 'width: 300px; height: 200px;'}),
        help_text="Select up to 7 O Line players. If you select less than 7, the others will be randomly generated."
    )
    d_line_players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 10, 'style': 'width: 300px; height: 200px;'}),
        help_text="Select up to 7 D Line players. If you select less than 7, the others will be randomly generated."
    )
    bench_players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 10, 'style': 'width: 300px; height: 200px;'}),
        help_text="Select up to 7 Bench players. If you select less than 7, the others will be randomly generated."
    )
    is_public = forms.BooleanField(
        required=False,
        help_text="Do you want to allow other users to see and use this?"
    )

    class Meta:
        model = Team
        exclude = ['players', 'created_by', 'overall_rating']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        user_profile = self.request.user.profile
        self.fields['o_line_players'].queryset = Player.objects.filter(
            Q(created_by=user_profile) | Q(is_public=True),
            primary_line='OFFENSE'
        )
        self.fields['d_line_players'].queryset = Player.objects.filter(
            Q(created_by=user_profile) | Q(is_public=True),
            primary_line='DEFENSE'
        )
        self.fields['bench_players'].queryset = Player.objects.filter(
            Q(created_by=user_profile) | Q(is_public=True),
            primary_line='BENCH'
        )

    def clean(self):
        cleaned_data = super().clean()
        o_line_players = cleaned_data.get('o_line_players')
        d_line_players = cleaned_data.get('d_line_players')
        bench_players = cleaned_data.get('bench_players')
        if o_line_players and len(o_line_players) > 7:
            raise forms.ValidationError("You cannot choose more than 7 O Line players")
        if d_line_players and len(d_line_players) > 7:
            raise forms.ValidationError("You cannot choose more than 7 D line players")
        if bench_players and len(bench_players) > 7:
            raise forms.ValidationError("You cannot choose more than 7 Bench players")
        return cleaned_data

    def save(self, commit=True):
        team = super().save(commit=False)
        team.created_by = self.request.user.profile
        if commit:
            team.save()
            # Assign the selected players to the team
            team.o_line_players.set(self.cleaned_data['o_line_players'])
            team.d_line_players.set(self.cleaned_data['d_line_players'])
            team.bench_players.set(self.cleaned_data['bench_players'])
            # Calculate and save the overall team rating
            team.overall_rating = calculate_overall_team_rating(team)
            team.save()
        return team


class TournamentForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 10, 'style': 'width: 300px; height: 200px;'}),
        help_text="Select multiple teams. If you don't select as many as will be in tourney, they will be randomly generated."
    )
    is_public = forms.BooleanField(
        required=False,
        help_text="Do you want to allow other users to see and use this?"
    )

    class Meta:
        model = Tournament
        fields = ['name', 'location', 'number_of_teams', 'simulation_type', 'is_public']
        exclude = ['created_by', 'pool_play_completed', 'bracket_play_completed']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        user_profile = self.request.user.profile
        self.fields['teams'].queryset = Team.objects.filter(Q(created_by=user_profile) | Q(is_public=True))
        self.fields['simulation_type'].initial = 'player_rating'
        self.fields['simulation_type'].widget.attrs['readonly'] = True
        self.fields['simulation_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        tournament = super().save(commit=False)
        tournament.created_by = self.request.user.profile

        if commit:
            tournament.save()
        return tournament

class GameForm(forms.ModelForm):
    is_public = forms.BooleanField(
        required=False,
        help_text="Do you want to allow other users to see and use this?"
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        print('request: ', self.request)
        super().__init__(*args, **kwargs)
        user_profile = self.request.user.profile
        # Filter to only teams created by this user
        self.fields['team_one'].queryset = Team.objects.filter(type='USAU')
        self.fields['team_two'].queryset = Team.objects.filter(type='USAU')

    class Meta:
        model = Game
        fields = ['team_one', 'team_two', 'date']
class UFAGameForm(forms.ModelForm):
    is_public = forms.BooleanField(
        required=False,
        help_text="Do you want to allow other users to see and use this?"
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        user_profile = self.request.user.profile
        # Filter to only teams created by this user
        self.fields['team_one'].queryset = Team.objects.filter(type='UFA')
        self.fields['team_two'].queryset = Team.objects.filter(type='UFA')

    class Meta:
        model = Game
        fields = ['team_one', 'team_two', 'date']


class UpdateTournamentTeamPoolPlaySeedForm(forms.ModelForm):
    class Meta:
        model = TournamentTeam
        fields = ['pool_play_seed']
