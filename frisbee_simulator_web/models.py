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
    PRIMARY_LINE_CHOICES = [
        ('OFFENSE', 'OFFENSE'),
        ('DEFENSE', 'DEFENSE'),
        ('BENCH', 'BENCH'),
    ]
    primary_line = models.CharField(max_length=50, choices=PRIMARY_LINE_CHOICES, null=True)
    PRIMARY_POSITION_CHOICES = [
        ('OFFENSE', 'OFFENSE'),
        ('DEFENSE', 'DEFENSE'),
        ('BENCH', 'BENCH'),
    ]
    primary_position = models.CharField(max_length=50, choices=PRIMARY_POSITION_CHOICES, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    teams = models.ManyToManyField('Team', related_name='teams_players')
    seasons = models.ManyToManyField('Season', related_name='seasons_players')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Team(models.Model):
    location = models.CharField(max_length=50, null=True)
    mascot = models.CharField(max_length=50, null=True)
    players = models.ManyToManyField(Player, related_name='players_teams')
    overall_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0,
                                                 null=True)
    o_line_players = models.ManyToManyField(Player, related_name='o_line_players_teams')
    d_line_players = models.ManyToManyField(Player, related_name='d_line_players_teams')
    o_line_handlers = models.ManyToManyField(Player, related_name='o_line_handlers_teams')
    d_line_handlers = models.ManyToManyField(Player, related_name='d_line_handlers_teams')
    o_line_cutters = models.ManyToManyField(Player, related_name='o_line_cutters_teams')
    d_line_cutters = models.ManyToManyField(Player, related_name='d_line_cutters_teams')
    o_line_hybrids = models.ManyToManyField(Player, related_name='o_line_hybrids_teams')
    d_line_hybrids = models.ManyToManyField(Player, related_name='d_line_hybrids_teams')
    bench_players = models.ManyToManyField(Player, related_name='bench_players_teams')
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.location + ' ' + self.mascot


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
        ('Exhibition', 'Exhibition')
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


class PlayerTournamentStat(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tournament_stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='player_tournament_stats', blank=True, null=True)
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
