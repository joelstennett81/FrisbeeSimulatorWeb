from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

import frisbee_simulator_web.views.teams
import frisbee_simulator_web.views.games
from frisbee_simulator_web.serializers import *
from frisbee_simulator_web.views.misc import *


class PlayerCreateView(CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]


class PlayerListView(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]


class PlayerDetailView(RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]


class PlayerUpdateView(UpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]


class TeamCreateView(CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class TeamListView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class TeamDetailView(RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class TeamUpdateView(UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class RandomTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        team = frisbee_simulator_web.views.teams.create_random_team(request)
        team.save()
        return Response({"message": "Random team created successfully"}, status=status.HTTP_201_CREATED)


class TeamListPublicView(ListAPIView):
    queryset = Team.objects.filter(is_public=True).order_by('created_by')
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class CreateIndividualGameView(CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile)


class SimulateIndividualGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        game = frisbee_simulator_web.views.games.perform_simulate_individual_game(request, game_id)
        return Response({"message": "Game simulated successfully"}, status=status.HTTP_200_OK)


class GamesListView(ListAPIView):
    queryset = Game.objects.filter(game_type='Exhibition').select_related('created_by')
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]


class ListPlayerTournamentStatsView(ListAPIView):
    serializer_class = PlayerTournamentStatSerializer

    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        return PlayerTournamentStat.objects.filter(tournament=tournament_id)


class DetailPlayerTournamentStatsView(RetrieveAPIView):
    serializer_class = PlayerTournamentStatSerializer

    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        player_id = self.kwargs.get('player_id')
        return PlayerTournamentStat.objects.filter(
            tournament__id=tournament_id,
            player__id=player_id
        )


class ListPlayerGameStatsView(ListAPIView):
    serializer_class = PlayerGameStatSerializer

    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        return PlayerGameStat.objects.filter(game__tournament__id=tournament_id)


class DetailPlayerGameStatsView(RetrieveAPIView):
    serializer_class = PlayerGameStatSerializer

    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        player_id = self.kwargs.get('player_id')
        return PlayerGameStat.objects.filter(
            game__tournament__id=tournament_id,
            player__id=player_id
        )


class ListTournamentsView(APIView):
    def get(self, request):
        tournaments = Tournament.objects.filter(created_by=request.user.profile)
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)


class CreateTournamentView(APIView):
    def post(self, request):
        form_data = request.data
        # Validate form data
        # Save tournament using form data
        # Return success message


class DeleteTournamentView(APIView):
    def delete(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        tournament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SimulateTournamentView(APIView):
    def get(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        # Implement simulation logic here
        return Response({"message": "Simulation completed"})


class PoolPlayOverviewView(APIView):
    def get(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        # Implement pool play overview logic here
        return Response({"pool_play_games": tournament.pool_play_games.all()})


class BracketOverviewView(APIView):
    def get(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        # Implement bracket overview logic here
        return Response({"bracket_rounds": tournament.bracket_rounds.all()})


class SimulateGameView(APIView):
    def post(self, request, game_id, tournament_id):
        game = Game.objects.get(id=game_id)
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement game simulation logic here
        return Response({"winner": game.winner.team.name, "loser": game.loser.team.name})


class CheckSimulationStatusView(APIView):
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        if tournament.pool_play_completed:
            return Response({"simulations_complete": True})
        else:
            return Response({"simulations_complete": False})


class FetchLatestGamesDataView(APIView):
    def get(self, request, tournament_id):
        games = Game.objects.filter(tournament__id=tournament_id)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


class SimulateFullPoolPlayView(APIView):
    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement full pool play simulation logic here
        return Response({"message": "Full pool play simulated"})


class SimulatePrequarterfinalRoundView(APIView):
    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement pre-quarterfinal round simulation logic here
        return Response({"message": "Pre-quarterfinal round simulated"})


class SimulateQuarterfinalRoundView(APIView):
    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement quarterfinal round simulation logic here
        return Response({"message": "Quarterfinal round simulated"})


class SimulateSemifinalRoundView(APIView):
    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement semifinal round simulation logic here
        return Response({"message": "Semifinal round simulated"})


class SimulateFinalRoundView(APIView):
    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement final round simulation logic here
        return Response({"champion": tournament.champion.team.name})


class SaveTournamentPlayerStatsView(APIView):
    def post(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement player stats saving logic here
        return Response({"message": "Player stats saved"})


class GetTournamentResultsView(APIView):
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        # Implement tournament results retrieval logic here
        return Response({"results": tournament.results})


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            profile = Profile.objects.create(user=user)

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'profile': ProfileSerializer(profile).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
        return Response({
            'token': token.key,
            'user': UserSerializer(serializer.validated_data['user']).data,
            'profile': ProfileSerializer(Profile.objects.get(user=serializer.validated_data['user'])).data
        })


class LogoutView(generics.GenericAPIView):
    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
