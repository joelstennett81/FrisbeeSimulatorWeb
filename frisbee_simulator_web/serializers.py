from rest_framework import serializers
from .models import *


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'created_by', 'is_public']  # Include all fields you want to expose via API


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name']


class TournamentTeamSerializer(serializers.ModelSerializer):
    team = TournamentSerializer(read_only=True)

    class Meta:
        model = TournamentTeam
        fields = ['id', 'team', 'tournament', 'pool_play_seed', 'bracket_play_seed']


class GameSerializer(serializers.ModelSerializer):
    t1 = TournamentTeamSerializer(read_only=True)
    t2 = TournamentTeamSerializer(read_only=True)
    winner = TournamentTeamSerializer(read_only=True)
    loser = TournamentTeamSerializer(read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Game
        fields = ['id', 't1', 't2', 'winner', 'loser', 'game_type', 'date', 'is_completed', 'created_by']


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'number_of_teams', 'created_by']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'tournament', 'team_one', 'team_two', 'winner', 'score']


class TournamentTeamSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField()

    class Meta:
        model = TournamentTeam
        fields = ['id', 'team', 'pool_play_wins', 'pool_play_losses', 'pool_play_point_differential']


class PlayerTournamentStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerTournamentStat
        fields = ['player', 'goals', 'assists', 'throwing_yards', 'receiving_yards', 'turnovers_forced']


class PlayerGameStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerGameStat
        fields = ['__all__']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'phonenumber', 'address']
