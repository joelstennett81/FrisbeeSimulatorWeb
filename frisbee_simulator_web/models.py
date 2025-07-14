import pytz
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    jersey_number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    height_in_inches = models.PositiveIntegerField(
        validators=[MinValueValidator(48), MaxValueValidator(90)])  # In inches
    weight_in_lbs = models.PositiveIntegerField(validators=[MinValueValidator(50), MaxValueValidator(450)])  # In pounds
    speed = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    jumping = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    agility = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    deep_huck_cut_defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                        default=65)
    short_huck_cut_defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                         default=65)
    under_cut_defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                    default=65)
    handle_mark_defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                      default=65)
    handle_cut_defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                     default=65)
    deep_huck_cut_offense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                        default=65)
    short_huck_cut_offense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                         default=65)
    under_cut_offense = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=65)
    handle_cut_offense = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=65)  # Not sure how to use it
    swing_throw_offense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                      default=65)
    under_throw_offense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                      default=65)
    short_huck_throw_offense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                           default=65)
    deep_huck_throw_offense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                          default=65)
    overall_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    overall_handle_offense_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    overall_handle_defense_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    overall_cutter_offense_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    overall_cutter_defense_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    is_public = models.BooleanField(default=False)
    year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)], blank=True, null=True)
    PRIMARY_LINE_CHOICES = [
        ('OFFENSE', 'OFFENSE'),
        ('DEFENSE', 'DEFENSE'),
        ('BENCH', 'BENCH'),
        ('DEEP_BENCH', 'DEEP BENCH')
    ]
    primary_line = models.CharField(max_length=50, choices=PRIMARY_LINE_CHOICES, null=True)
    PRIMARY_POSITION_CHOICES = [
        ('OFFENSE', 'OFFENSE'),
        ('DEFENSE', 'DEFENSE'),
        ('BENCH', 'BENCH'),
        ('DEEP_BENCH', 'DEEP BENCH')
    ]
    primary_position = models.CharField(max_length=50, choices=PRIMARY_POSITION_CHOICES, blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    teams = models.ManyToManyField('Team', related_name='teams_players', blank=True, null=True)
    seasons = models.ManyToManyField('Season', related_name='seasons_players', blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def calculate_all_overall_ratings(self):
        import frisbee_simulator_web.views.misc as misc
        self.overall_rating = misc.calculate_overall_player_rating(self)
        self.overall_handle_offense_rating = misc.calculate_handle_offense_rating(self)
        self.overall_handle_defense_rating = misc.calculate_handle_defense_rating(self)
        self.overall_cutter_offense_rating = misc.calculate_cutter_offense_rating(self)
        self.overall_cutter_defense_rating = misc.calculate_cutter_defense_rating(self)


class Team(models.Model):
    TYPES = [
        ('UFA', 'UFA'),
        ('USAU', 'USAU'),
    ]
    type = models.CharField(max_length=50, choices=TYPES, null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    mascot = models.CharField(max_length=50, null=True, blank=True)
    players = models.ManyToManyField(Player, related_name='players_teams', blank=True)
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, null=True, blank=True
    )
    o_line_players = models.ManyToManyField(Player, related_name='o_line_players_teams', blank=True)
    d_line_players = models.ManyToManyField(Player, related_name='d_line_players_teams', blank=True)
    o_line_handlers = models.ManyToManyField(Player, related_name='o_line_handlers_teams', blank=True)
    d_line_handlers = models.ManyToManyField(Player, related_name='d_line_handlers_teams', blank=True)
    o_line_cutters = models.ManyToManyField(Player, related_name='o_line_cutters_teams', blank=True)
    d_line_cutters = models.ManyToManyField(Player, related_name='d_line_cutters_teams', blank=True)
    o_line_hybrids = models.ManyToManyField(Player, related_name='o_line_hybrids_teams', blank=True)
    d_line_hybrids = models.ManyToManyField(Player, related_name='d_line_hybrids_teams', blank=True)
    bench_players = models.ManyToManyField(Player, related_name='bench_players_teams', blank=True)
    bench_handlers = models.ManyToManyField(Player, related_name='bench_handlers_teams', blank=True)
    bench_cutters = models.ManyToManyField(Player, related_name='bench_cutters_teams', blank=True)
    deep_bench_players = models.ManyToManyField(Player, related_name='deep_bench_players_teams', blank=True)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)], blank=True, null=True)

    def __str__(self):
        return f"{self.location or ''} {self.mascot or ''}".strip()


class Season(models.Model):
    SEASON_TYPE_CHOICES = [
        ('College Fall', 'College Fall'),
        ('College Spring', 'College Spring'),
        ('Club', 'Club'),
        ('AUDL', 'AUDL'),
        ('PUL', 'PUL')
    ]
    season_type = models.CharField(max_length=50, choices=SEASON_TYPE_CHOICES)
    year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)])
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    teams = models.ManyToManyField(Team, related_name='teams_seasons')
    players = models.ManyToManyField(Player, related_name='players_seasons')


class Tournament(models.Model):
    NUMBER_OF_TEAMS_CHOICES = [
        (4, '4'),
        (8, '8'),
        (16, '16'),
        (20, '20')
    ]
    SIMULATION_TYPE_CHOICES = [
        ('player_rating', 'player_rating'),
        ('team_rating', 'team_rating')
    ]
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    number_of_teams = models.PositiveIntegerField(choices=NUMBER_OF_TEAMS_CHOICES, default=4)
    simulation_type = models.CharField(choices=SIMULATION_TYPE_CHOICES, default='player_rating')
    teams = models.ManyToManyField(Team, related_name='teams_tournaments')
    champion = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    is_complete = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    pool_play_games_completed_counter = models.PositiveIntegerField(default=0, null=True)
    pool_play_total_number_of_games = models.PositiveIntegerField(default=0, null=True)
    pool_play_completed = models.BooleanField(default=False)
    pre_quarterfinal_round_completed = models.BooleanField(default=False)
    quarterfinal_round_completed = models.BooleanField(default=False)
    losers_quarterfinal_round_completed = models.BooleanField(default=False)
    semifinal_round_completed = models.BooleanField(default=False)
    losers_semifinal_round_completed = models.BooleanField(default=False)
    final_round_completed = models.BooleanField(default=False)
    losers_final_round_completed = models.BooleanField(default=False)
    pool_play_initialized = models.BooleanField(default=False)
    pre_quarterfinal_round_initialized = models.BooleanField(default=False)
    quarterfinal_round_initialized = models.BooleanField(default=False)
    losers_quarterfinal_round_initialized = models.BooleanField(default=False)
    semifinal_round_initialized = models.BooleanField(default=False)
    losers_semifinal_round_initialized = models.BooleanField(default=False)
    final_round_initialized = models.BooleanField(default=False)
    losers_final_round_initialized = models.BooleanField(default=False)
    pool_play_games = models.ManyToManyField('Game', related_name='pool_play_games_tournament')
    pre_quarterfinal_round_games = models.ManyToManyField('Game', related_name='prequarter_final_games_tournament')
    quarterfinal_round_games = models.ManyToManyField('Game', related_name='quarterfinal_games_tournament')
    losers_quarterfinal_round_games = models.ManyToManyField('Game',
                                                             related_name='losers_quarterfinal_games_tournament')
    semifinal_round_games = models.ManyToManyField('Game', related_name='semifinal_games_tournament')
    losers_semifinal_round_games = models.ManyToManyField('Game', related_name='losers_semifinal_games_tournament')
    final_round_games = models.ManyToManyField('Game', related_name='final_games_tournament')
    losers_final_round_games = models.ManyToManyField('Game', related_name='losers_final_games_tournament')
    pool_play_seeds_set = models.BooleanField(default=False)

    def total_pool_play_games(self):
        num_teams = self.teams.count()
        if num_teams == 4:
            return 6
        elif num_teams == 8:
            return 12
        # Add more conditions here if you support more team counts
        else:
            return 0


class TournamentPool(models.Model):
    POOL_SIZE_CHOICES = [
        (4, '4'),
        (5, '5'),
    ]
    name = models.CharField(max_length=50, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    teams = models.ManyToManyField('TournamentTeam', related_name='teams_pools')
    number_of_teams = models.PositiveIntegerField(choices=POOL_SIZE_CHOICES, default=4)


class TournamentBracket(models.Model):
    BRACKET_SIZE_CHOICES = [
        (4, '4'),
        (8, '8'),
        (16, '16')
    ]
    BRACKET_TYPE_CHOICES = [
        ('Championship', 'Championship'),
        ('Loser', 'Loser'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    teams = models.ManyToManyField('TournamentTeam', related_name='teams_brackets')
    number_of_teams = models.PositiveIntegerField(choices=BRACKET_SIZE_CHOICES, default=4)
    bracket_type = models.CharField(max_length=50, choices=BRACKET_TYPE_CHOICES)
    champion = models.ForeignKey('TournamentTeam', on_delete=models.CASCADE, null=True)


class TournamentTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    pool_play_seed = models.PositiveIntegerField()
    bracket_play_seed = models.PositiveIntegerField(blank=True)
    pool = models.ForeignKey(TournamentPool, on_delete=models.CASCADE, null=True)
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE, null=True)
    pool_play_wins = models.PositiveIntegerField(default=0)
    pool_play_losses = models.PositiveIntegerField(default=0)
    pool_play_point_differential = models.IntegerField(default=0)
    bracket_play_wins = models.PositiveIntegerField(default=0)
    bracket_play_losses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '(' + str(self.pool_play_seed) + ') ' + self.team.location + ' ' + self.team.mascot

    def unseeded_name(self):
        return self.team.location + ' ' + self.team.mascot


class Game(models.Model):
    GAME_TYPE_CHOICES = [
        ('Pool Play', 'Pool Play'),
        ('Pre-Quarterfinal', 'Pre-Quarterfinal'),
        ('Quarterfinal', 'Quarterfinal'),
        ('Semifinal', 'Semifinal'),
        ('Championship', 'Championship'),
        ('3rd-Place Final', '3rd-Place Final'),
        ('5th-Place Semifinal', '5th-Place Semifinal'),
        ('5th-Place Final', '5th-Place Final'),
        ('7th-Place Final', '7th-Place Final'),
        ('9th-Place Quarterfinal', '9th-Place Quarterfinal'),
        ('9th-Place Semifinal', '9th-Place Semifinal'),
        ('9th-Place Final', '9th-Place Final'),
        ('11th-Place Final', '11th-Place Final'),
        ('13th-Place Semifinal', '13th-Place Semifinal'),
        ('13th-Place Final', '13th-Place Final'),
        ('15th-Place Final', '15th-Place Final'),
        ('17th-Place Semifinal', '17th-Place Semifinal'),
        ('17th-Place Final', '17th-Place Final'),
        ('19th-Place Final', '19th-Place Final'),
        ('Exhibition', 'Exhibition'),
        ('UFA', 'UFA')
    ]
    date = models.DateTimeField(default=timezone.now)
    team_one = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='team_one_games')
    team_two = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='team_two_games')
    pool = models.ForeignKey(TournamentPool, on_delete=models.CASCADE, null=True)
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games', null=True)
    game_type = models.CharField(max_length=50, choices=GAME_TYPE_CHOICES, default='Exhibition')
    winner = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='winner_games', null=True)
    loser = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='loser_games', null=True)
    winner_score = models.PositiveIntegerField(default=0)
    loser_score = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)


class UFASeason(models.Model):
    SIMULATION_TYPE_CHOICES = [
        ('player_rating', 'player_rating'),
        ('team_rating', 'team_rating')
    ]
    name = models.CharField(max_length=50)
    year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)])
    number_of_teams = models.PositiveIntegerField(default=24)
    simulation_type = models.CharField(choices=SIMULATION_TYPE_CHOICES, default='player_rating')
    teams = models.ManyToManyField(Team, related_name='teams_season')
    champion = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)


class UFASeasonTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(UFASeason, on_delete=models.CASCADE)
    division = models.ForeignKey('UFADivision', on_delete=models.CASCADE)
    regular_season_wins = models.PositiveIntegerField(default=0)
    regular_season_losses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.team.location + ' ' + self.team.mascot


class UFASeasonGame(models.Model):
    GAME_TYPE_CHOICES = [
        ('Exhibition', 'Exhibition'),
        ('Regular Season', 'Regular Season')
    ]
    date = models.DateTimeField(default=timezone.now)
    team_one = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='team_one_games')
    team_two = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='team_two_games')
    game_type = models.CharField(max_length=50, choices=GAME_TYPE_CHOICES, default='Exhibition')
    winner = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='winner_games', null=True)
    loser = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='loser_games', null=True)
    winner_score = models.PositiveIntegerField(default=0)
    loser_score = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(UFASeason, on_delete=models.CASCADE, blank=True, null=True)


class Point(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_points')
    team_one = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='team_one_points')
    team_two = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='team_two_points')
    winner = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='winner_points', null=True)
    loser = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='loser_points', null=True)
    point_number_in_game = models.PositiveIntegerField(default=0)
    print_statements = models.CharField(max_length=50000, null=True)
    team_one_score_post_point = models.IntegerField(default=0)
    team_two_score_post_point = models.IntegerField(default=0)

class UFAPoint(models.Model):
    game = models.ForeignKey(UFASeasonGame, on_delete=models.CASCADE, related_name='ufa_game_points')
    team_one = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='ufa_team_one_points')
    team_two = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='ufa_team_two_points')
    winner = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='ufa_winner_points', null=True)
    loser = models.ForeignKey(UFASeasonTeam, on_delete=models.CASCADE, related_name='ufa_loser_points', null=True)
    point_number_in_game = models.PositiveIntegerField(default=0)
    print_statements = models.CharField(max_length=50000, null=True)
    team_one_score_post_point = models.IntegerField(default=0)
    team_two_score_post_point = models.IntegerField(default=0)


class PlayerPointStat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='point_stats_for_game')
    point = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='point_stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    swing_passes_thrown = models.PositiveIntegerField(default=0)
    swing_passes_completed = models.PositiveIntegerField(default=0)
    under_passes_thrown = models.PositiveIntegerField(default=0)
    under_passes_completed = models.PositiveIntegerField(default=0)
    short_hucks_thrown = models.PositiveIntegerField(default=0)
    short_hucks_completed = models.PositiveIntegerField(default=0)
    deep_hucks_thrown = models.PositiveIntegerField(default=0)
    deep_hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)

class UFAPlayerPointStat(models.Model):
    game = models.ForeignKey(UFASeasonGame, on_delete=models.CASCADE, related_name='ufa_point_stats_for_game')
    point = models.ForeignKey(UFAPoint, on_delete=models.CASCADE, related_name='ufa_player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ufa_point_stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    swing_passes_thrown = models.PositiveIntegerField(default=0)
    swing_passes_completed = models.PositiveIntegerField(default=0)
    under_passes_thrown = models.PositiveIntegerField(default=0)
    under_passes_completed = models.PositiveIntegerField(default=0)
    short_hucks_thrown = models.PositiveIntegerField(default=0)
    short_hucks_completed = models.PositiveIntegerField(default=0)
    deep_hucks_thrown = models.PositiveIntegerField(default=0)
    deep_hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)


class PlayerGameStat(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='game_stats_for_tournament',
                                   null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='game_stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    swing_passes_thrown = models.PositiveIntegerField(default=0)
    swing_passes_completed = models.PositiveIntegerField(default=0)
    under_passes_thrown = models.PositiveIntegerField(default=0)
    under_passes_completed = models.PositiveIntegerField(default=0)
    short_hucks_thrown = models.PositiveIntegerField(default=0)
    short_hucks_completed = models.PositiveIntegerField(default=0)
    deep_hucks_thrown = models.PositiveIntegerField(default=0)
    deep_hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)


class UFAPlayerGameStat(models.Model):
    season = models.ForeignKey(UFASeason, on_delete=models.CASCADE, related_name='ufa_game_stats_for_season',
                               null=True)
    game = models.ForeignKey(UFASeasonGame, on_delete=models.CASCADE, related_name='ufa_player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ufa_game_stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    swing_passes_thrown = models.PositiveIntegerField(default=0)
    swing_passes_completed = models.PositiveIntegerField(default=0)
    under_passes_thrown = models.PositiveIntegerField(default=0)
    under_passes_completed = models.PositiveIntegerField(default=0)
    short_hucks_thrown = models.PositiveIntegerField(default=0)
    short_hucks_completed = models.PositiveIntegerField(default=0)
    deep_hucks_thrown = models.PositiveIntegerField(default=0)
    deep_hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)


class PlayerTournamentStat(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tournament_stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='player_tournament_stats', blank=True,
                             null=True)
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    swing_passes_thrown = models.PositiveIntegerField(default=0)
    swing_passes_completed = models.PositiveIntegerField(default=0)
    under_passes_thrown = models.PositiveIntegerField(default=0)
    under_passes_completed = models.PositiveIntegerField(default=0)
    short_hucks_thrown = models.PositiveIntegerField(default=0)
    short_hucks_completed = models.PositiveIntegerField(default=0)
    deep_hucks_thrown = models.PositiveIntegerField(default=0)
    deep_hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)


class UFAPlayerSeasonStat(models.Model):
    season = models.ForeignKey(UFASeason, on_delete=models.CASCADE, related_name='ufa_player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ufa_season_stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='ufa_player_season_stats', blank=True,
                             null=True)
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    swing_passes_thrown = models.PositiveIntegerField(default=0)
    swing_passes_completed = models.PositiveIntegerField(default=0)
    under_passes_thrown = models.PositiveIntegerField(default=0)
    under_passes_completed = models.PositiveIntegerField(default=0)
    short_hucks_thrown = models.PositiveIntegerField(default=0)
    short_hucks_completed = models.PositiveIntegerField(default=0)
    deep_hucks_thrown = models.PositiveIntegerField(default=0)
    deep_hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)


class PlayerSeasonStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='season_stats')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='player_stats')


class TeamGameStat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='team_stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='game_stats')
    goals_scored = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    passes_thrown = models.PositiveIntegerField(default=0)
    passes_completed = models.PositiveIntegerField(default=0)
    hucks_thrown = models.PositiveIntegerField(default=0)
    hucks_completed = models.PositiveIntegerField(default=0)
    total_throwing_yards = models.IntegerField(default=0)
    total_receiving_yards = models.IntegerField(default=0)
    turnovers = models.PositiveIntegerField(default=0)


class TeamTournamentStat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tournament_stats')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='team_stats')
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    passing_yards_for = models.IntegerField(default=0)
    passing_yards_against = models.IntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    passes_thrown = models.PositiveIntegerField(default=0)
    passes_completed = models.PositiveIntegerField(default=0)
    hucks_thrown = models.PositiveIntegerField(default=0)
    hucks_completed = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)


class TeamSeasonStat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='season_stats')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='team_season_stats')
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()


# UFA Models
class UFATeam(models.Model):
    ufa_id = models.CharField(max_length=50, unique=True)
    year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)])
    division = models.ForeignKey('UFADivision', on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=3)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    standing = models.IntegerField()

    def __str__(self):
        return f"{self.full_name} ({self.city})"


class UFADivision(models.Model):
    ufa_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UFAPlayer(models.Model):
    ufa_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    teams = models.ManyToManyField('UFATeam', through='UFAPlayerTeam')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UFAPlayerTeam(models.Model):
    player = models.ForeignKey(UFAPlayer, on_delete=models.CASCADE)
    team = models.ForeignKey('UFATeam', on_delete=models.CASCADE)
    active = models.BooleanField()
    year = models.IntegerField()
    jersey_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'team', 'year'],
                condition=models.Q(active=True),
                name='unique_active_ufa_player_team'
            ),
        ]

    def __str__(self):
        return f"{self.player} on {self.team} ({self.year})"


class UFAGame(models.Model):
    ufa_id = models.CharField(max_length=50, unique=True)
    away_team = models.ForeignKey('UFATeam', on_delete=models.CASCADE, related_name='away_games')
    home_team = models.ForeignKey('UFATeam', on_delete=models.CASCADE, related_name='home_games')
    away_score = models.IntegerField(null=True, blank=True)
    home_score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50)  # Updated to match API status options
    start_timestamp = models.DateTimeField()
    start_timezone = models.CharField(max_length=50)
    streaming_url = models.URLField(max_length=200, null=True, blank=True)
    update_timestamp = models.DateTimeField()
    week = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.away_team} vs {self.home_team} - {self.start_timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def start_datetime(self):
        return self.start_timestamp.replace(tzinfo=pytz.FixedOffset(0))

    @property
    def formatted_start_datetime(self):
        return self.start_datetime.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S%z')

    @property
    def formatted_update_datetime(self):
        return self.update_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


class UFAGameEvent(models.Model):
    ufa_id = models.CharField(max_length=50, unique=True)
    game = models.ForeignKey(UFAGame, on_delete=models.CASCADE, related_name='events')
    type = models.IntegerField()
    line = models.JSONField()  # Assuming line is a JSON array of player names
    time = models.FloatField()

    def __str__(self):
        return f"Event in {self.game}: Type {self.type}, Time {self.time}"


class UFAPlayerStatsYear(models.Model):
    player = models.OneToOneField(UFAPlayer, on_delete=models.CASCADE, primary_key=True)
    year = models.IntegerField()
    assists = models.IntegerField()
    goals = models.IntegerField()
    hockey_assists = models.IntegerField()
    completions = models.IntegerField()
    throw_attempts = models.IntegerField()
    throwaways = models.IntegerField()
    stalls = models.IntegerField()
    callahans_thrown = models.IntegerField()
    yards_received = models.IntegerField()
    yards_thrown = models.IntegerField()
    hucks_attempted = models.IntegerField()
    hucks_completed = models.IntegerField()
    catches = models.IntegerField()
    drops = models.IntegerField()
    blocks = models.IntegerField()
    callahans_caught = models.IntegerField()
    pulls = models.IntegerField()
    ob_pulls = models.IntegerField()
    recorded_pulls = models.IntegerField()
    recorded_pulls_hangtime = models.IntegerField()
    o_points_played = models.IntegerField()
    o_points_scored = models.IntegerField()
    d_points_played = models.IntegerField()
    d_points_scored = models.IntegerField()
    seconds_played = models.IntegerField()
    o_opportunities = models.IntegerField()
    o_opportunity_scores = models.IntegerField()
    d_opportunities = models.IntegerField()
    d_opportunity_stops = models.IntegerField()

    def __str__(self):
        return f"{self.player}'s stats for {self.year}"
