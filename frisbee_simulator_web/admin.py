import time
from collections import defaultdict

import requests
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
import numpy as np
import random

from .models import *
from django.db import transaction

UFA_API_BASE = "https://api.theaudl.com/api/v1"


@admin.register(PlayerGameStat)
class PlayerGameStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'get_game_date', 'goals', 'assists', 'throwing_yards', 'receiving_yards')
    search_fields = ('player__first_name', 'player__last_name')
    list_filter = ('game',)

    def get_game_date(self, obj):
        return obj.game.date if obj.game else "-"

    get_game_date.short_description = 'Game Date'


@admin.register(PlayerPointStat)
class PlayerPointStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'get_game_date', 'get_point_number', 'goals', 'assists', 'throwaways', 'drops')
    search_fields = ('player__first_name', 'player__last_name')
    list_filter = ('game',)

    def get_game_date(self, obj):
        return obj.game.date if obj.game else "-"

    get_game_date.short_description = 'Game Date'

    def get_point_number(self, obj):
        return obj.point.number if obj.point else "-"

    get_point_number.short_description = 'Point #'


@admin.register(PlayerSeasonStat)
class PlayerSeasonStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'season')


@admin.register(PlayerTournamentStat)
class PlayerTournamentStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'tournament', 'goals', 'assists', 'throwing_yards', 'receiving_yards')
    search_fields = ('player__first_name', 'player__last_name')


@admin.register(UFAPlayerGameStat)
class UFAPlayerGameStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'get_game_date', 'goals', 'assists', 'throwing_yards', 'receiving_yards')
    search_fields = ('player__first_name', 'player__last_name')

    def get_game_date(self, obj):
        return obj.game.date if obj.game else "-"

    get_game_date.short_description = 'Game Date'


@admin.register(UFAPlayerPointStat)
class UFAPlayerPointStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'get_game_date', 'get_point_number', 'goals', 'assists', 'throwaways', 'drops')
    search_fields = ('player__first_name', 'player__last_name')

    def get_game_date(self, obj):
        return obj.game.date if obj.game else "-"

    get_game_date.short_description = 'Game Date'

    def get_point_number(self, obj):
        return obj.point.number if obj.point else "-"

    get_point_number.short_description = 'Point #'


@admin.register(UFAPlayerSeasonStat)
class UFAPlayerSeasonStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'season', 'goals', 'assists', 'throwing_yards', 'receiving_yards')
    search_fields = ('player__first_name', 'player__last_name')


@admin.register(UFASeasonGame)
class UFASeasonGameAdmin(admin.ModelAdmin):
    list_display = ('date', 'team_one', 'team_two', 'winner', 'winner_score', 'loser_score', 'is_completed')
    list_filter = ('is_completed', 'game_type')
    search_fields = ('team_one__team__location', 'team_two__team__location')


def fetch_and_update_players(modeladmin, request, queryset):
    """Fetch and update a Player from the API using their ufa_id."""
    url = "https://www.backend.ufastats.com/api/v1/players"
    params = {'years': '2025'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        players_data = response.json()

        for api_player in players_data['data']:
            ufa_id = api_player['playerID']
            first_name = api_player['firstName']
            last_name = api_player['lastName']
            teams = api_player['teams']
            player, created = UFAPlayer.objects.update_or_create(ufa_id=ufa_id,
                                                                 defaults={"first_name": first_name,
                                                                           "last_name": last_name})

            for api_team in teams:
                team = UFATeam.objects.get(ufa_id=api_team['teamID'])
                player_team, player_team_created = UFAPlayerTeam.objects.update_or_create(team=team, player=player,
                                                                                          active=True,
                                                                                          defaults={
                                                                                              "year": api_team['year'],
                                                                                              "jersey_number": api_team[
                                                                                                  "jerseyNumber"]})

    except Exception as e:
        messages.error(request, f"Error fetching players: {str(e)}")


@admin.action(description="Fetch and Update Teams")
def fetch_and_update_teams(modeladmin, request, queryset):
    url = "https://www.backend.ufastats.com/api/v1/teams"

    params = {'years': '2025'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        teams_data = response.json()

        for team_data in teams_data['data']:
            ufa_id = team_data['teamID']
            year = team_data['year']
            city = team_data['city']
            name = team_data['name']
            full_name = team_data['fullName']
            abbreviation = team_data['abbrev']
            wins = team_data['wins']
            losses = team_data['losses']
            ties = team_data['ties']
            standing = team_data['standing']
            division_id = team_data['division']['divisionID']
            division_name = team_data['division']['name']
            division, _ = UFADivision.objects.get_or_create(ufa_id=division_id, defaults={'name': division_name})
            existing_team, created = UFATeam.objects.update_or_create(
                ufa_id=ufa_id,
                defaults={"year": year, "division": division, "city": city, "name": name, "full_name": full_name,
                          "abbreviation": abbreviation, "wins": wins, "losses": losses, "ties": ties,
                          "standing": standing}
            )

            if created:
                messages.info(request, f"Created new team: {name}")
            else:
                messages.info(request, f"Updated existing team: {name}")

            existing_team.save()

        messages.success(request, "Teams fetched and updated successfully.")
    except Exception as e:
        messages.error(request, f"Error fetching teams: {str(e)}")


def fetch_and_update_games(modeladmin, request, queryset):
    url = "https://www.backend.ufastats.com/api/v1/games"
    params = {'date': '2025-01-01:2025-12-31'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        games_data = response.json()

        for api_game in games_data['data']:
            ufa_id = api_game['gameID']
            away_team_id = api_game['awayTeamID']
            home_team_id = api_game['homeTeamID']
            away_score = api_game['awayScore']
            home_score = api_game['homeScore']
            status = api_game['status']
            start_timestamp = api_game['startTimestamp']
            start_timezone = api_game['startTimezone']
            streaming_url = api_game['streamingURL']
            update_timestamp = api_game['updateTimestamp']
            week = api_game['week']

            away_team = UFATeam.objects.get(ufa_id=away_team_id)
            home_team = UFATeam.objects.get(ufa_id=home_team_id)

            game, created = UFAGame.objects.update_or_create(ufa_id=ufa_id,
                                                             defaults={"away_team": away_team, "home_team": home_team,
                                                                       "away_score": away_score,
                                                                       "home_score": home_score,
                                                                       "status": status,
                                                                       "start_timestamp": start_timestamp,
                                                                       "update_timestamp": update_timestamp,
                                                                       "week": week,
                                                                       "start_timezone": start_timezone,
                                                                       "streaming_url": streaming_url})
    except Exception as e:
        messages.error(request, f"Error fetching games: {str(e)}")


@admin.action(description="Fetch and Update Player Year Stats (Optimized)")
def fetch_and_update_year_stats(modeladmin, request, queryset):
    url = "https://www.backend.ufastats.com/api/v1/playerStats"
    BATCH_SIZE = 100
    YEAR = 2025
    errors = []

    # Cache all existing players by ufa_id
    ufa_player_map = {
        str(p.ufa_id): p for p in UFAPlayer.objects.all()
    }

    # Cache players to avoid repeated queries
    player_ids = list(ufa_player_map.keys())

    # Stats to bulk insert
    stats_to_insert = []

    # Begin batching
    for i in range(0, len(player_ids), BATCH_SIZE):
        batch_ids = player_ids[i:i + BATCH_SIZE]
        params = {'playerIDs': ','.join(batch_ids), 'years': [YEAR]}

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            stats_data = response.json().get('data', [])

            for api_stat in stats_data:
                api_player = api_stat['player']
                ufa_id = str(api_player['playerID'])
                player = ufa_player_map.get(ufa_id)

                if not player:
                    player = UFAPlayer.objects.create(
                        ufa_id=ufa_id,
                        first_name=api_player['firstName'],
                        last_name=api_player['lastName']
                    )
                    ufa_player_map[ufa_id] = player

                # Build the stat object
                stats_to_insert.append(UFAPlayerStatsYear(
                    player=player,
                    year=api_stat['year'],
                    assists=api_stat['assists'],
                    goals=api_stat['goals'],
                    hockey_assists=api_stat['hockeyAssists'],
                    completions=api_stat['completions'],
                    throw_attempts=api_stat['throwAttempts'],
                    throwaways=api_stat['throwaways'],
                    stalls=api_stat['stalls'],
                    callahans_thrown=api_stat['callahansThrown'],
                    yards_received=api_stat['yardsReceived'],
                    yards_thrown=api_stat['yardsThrown'],
                    hucks_attempted=api_stat['hucksAttempted'],
                    hucks_completed=api_stat['hucksCompleted'],
                    catches=api_stat['catches'],
                    drops=api_stat['drops'],
                    blocks=api_stat['blocks'],
                    callahans_caught=api_stat['callahans'],
                    pulls=api_stat['pulls'],
                    recorded_pulls=api_stat['recordedPulls'],
                    ob_pulls=api_stat['obPulls'],
                    recorded_pulls_hangtime=api_stat['recordedPullsHangtime'],
                    o_points_played=api_stat['oPointsPlayed'],
                    o_points_scored=api_stat['oPointsScored'],
                    d_points_played=api_stat['dPointsPlayed'],
                    d_points_scored=api_stat['dPointsScored'],
                    seconds_played=api_stat['secondsPlayed'],
                    o_opportunities=api_stat['oOpportunities'],
                    o_opportunity_scores=api_stat['oOpportunityScores'],
                    d_opportunities=api_stat['dOpportunities'],
                    d_opportunity_stops=api_stat['dOpportunityStops'],
                ))

        except Exception as e:
            errors.append(f"Batch {i // BATCH_SIZE}: {str(e)}")

    # Delete existing year stats in one go
    UFAPlayerStatsYear.objects.filter(year=YEAR).delete()

    # Bulk insert all new stats
    with transaction.atomic():
        UFAPlayerStatsYear.objects.bulk_create(stats_to_insert, batch_size=1000)

    # Notify
    messages.success(request, f"Inserted {len(stats_to_insert)} player year stats.")
    if errors:
        messages.error(request, f"{len(errors)} errors occurred. Example: {errors[0]}")


def create_teams_from_ufa_teams(modeladmin, request, queryset):
    ufa_teams = UFATeam.objects.filter(year=2025)

    for ufa_team in ufa_teams:
        team, created = Team.objects.update_or_create(
            location=ufa_team.city,
            mascot=ufa_team.name,
            type="UFA",
            is_public=True,
            year=ufa_team.year,
            ufa_team=ufa_team
        )

        # Get UFA players on that team
        ufa_player_ids = UFAPlayerTeam.objects.filter(
            team=ufa_team,
            year=2025,
            active=True
        ).values_list('player_id', flat=True)

        # Match to Player instances by name
        matched_players = Player.objects.filter(ufa_player__in=ufa_player_ids)
        # Assign to the team
        team.players.set(matched_players)
        team.save()


def setup_ufa_season(modeladmin, request, queryset):
    ufa_teams = UFATeam.objects.filter(year=2025)
    season, created = UFASeason.objects.update_or_create(name='2025 Season', year=2025, number_of_teams=24)

    for ufa_team in ufa_teams:
        api_team = Team.objects.get(year=2025, location=ufa_team.city, mascot=ufa_team.name)
        team, created = UFASeasonTeam.objects.update_or_create(
            team=api_team,
            season=season,
            division=ufa_team.division,
        )


def assign_primary_lines_for_team(team):
    players = list(team.players.all())

    # Fetch UFA stats for each player
    ufa_stats_map = {
        stat.player_id: stat for stat in UFAPlayerStatsYear.objects.filter(
            year=2025,
            player__in=[p.ufa_player for p in players if p.ufa_player]
        )
    }

    # Score by points played
    player_stats = []
    for player in players:
        ufa_player = player.ufa_player
        if not ufa_player:
            continue
        stat = ufa_stats_map.get(ufa_player.id)
        if not stat:
            continue

        o_points = stat.o_points_played or 0
        d_points = stat.d_points_played or 0
        total = o_points + d_points
        player_stats.append((player, o_points, d_points, total))
    # Sort by points played
    offense_line = sorted(player_stats, key=lambda x: x[1], reverse=True)[:7]
    offense_players = {x[0] for x in offense_line}

    remaining = [x for x in player_stats if x[0] not in offense_players]
    defense_line = sorted(remaining, key=lambda x: x[2], reverse=True)[:7]
    defense_players = {x[0] for x in defense_line}

    remaining = [x for x in remaining if x[0] not in defense_players]
    bench_line = sorted(remaining, key=lambda x: x[3], reverse=True)[:7]
    bench_players = {x[0] for x in bench_line}

    used_players = offense_players | defense_players | bench_players
    deep_bench_line = sorted(
        [x for x in player_stats if x[0] not in used_players],
        key=lambda x: x[3],
        reverse=True
    )[:7]
    deep_bench_players = {x[0] for x in deep_bench_line}

    # Save line assignments
    team.o_line_players.set(offense_players)
    team.d_line_players.set(defense_players)
    team.bench_players.set(bench_players)
    team.deep_bench_players.set(deep_bench_players)

    # Handler/cutter roles (default to cutter if not in top 3 handlers)
    o_handlers = sorted(offense_players, key=lambda p: p.overall_handle_offense_rating, reverse=True)[:3]
    d_handlers = sorted(defense_players, key=lambda p: p.overall_handle_defense_rating, reverse=True)[:3]
    bench_handlers = sorted(bench_players, key=lambda p: p.overall_handle_offense_rating, reverse=True)[:3]
    o_cutters = [p for p in offense_players if p not in o_handlers][:4]
    d_cutters = [p for p in defense_players if p not in d_handlers][:4]
    bench_cutters = [p for p in bench_players if p not in bench_handlers][:4]

    team.o_line_handlers.set(o_handlers)
    team.d_line_handlers.set(d_handlers)
    team.bench_handlers.set(bench_handlers)
    team.o_line_cutters.set(o_cutters)
    team.d_line_cutters.set(d_cutters)
    team.bench_cutters.set(bench_cutters)
    team.save()

    # Save primary line/position to Player model
    updates = []
    for p in players:
        if p in offense_players:
            p.primary_line = 'OFFENSE'
            p.primary_position = 'OFFENSE'
        elif p in defense_players:
            p.primary_line = 'DEFENSE'
            p.primary_position = 'DEFENSE'
        elif p in bench_players:
            p.primary_line = 'BENCH'
            p.primary_position = 'DEFENSE'
        elif p in deep_bench_players:
            p.primary_line = 'DEEP_BENCH'
            p.primary_position = 'DEEP_BENCH'
        else:
            p.primary_line = 'DEEP_BENCH'
            p.primary_position = 'DEEP_BENCH'
        updates.append(p)

    Player.objects.bulk_update(updates, ['primary_line', 'primary_position'])


def update_team_lines(modeladmin, request, queryset):
    from .views.misc import calculate_overall_team_rating
    for team in Team.objects.all():
        assign_primary_lines_for_team(team)
        team.overall_rating = calculate_overall_team_rating(team)
        team.save()


def curved_normalize(val, all_vals, mean=80, std=10, min_score=65, max_score=95):
    mu = np.mean(all_vals)
    sigma = np.std(all_vals) or 1
    z = (val - mu) / sigma
    score = mean + z * std
    return int(max(min(score, max_score), min_score))


def bulk_update_player_skills():
    skill_map = {
        "deep_huck_cut_defense": ["blocks"],
        "short_huck_cut_defense": ["blocks"],
        "under_cut_defense": ["blocks"],
        "handle_mark_defense": ["blocks"],
        "handle_cut_defense": ["blocks", "callahans_caught"],
        "deep_huck_cut_offense": ["yards_received", "goals"],
        "short_huck_cut_offense": ["yards_received", "goals"],
        "under_cut_offense": ["catches", "yards_received", "goals", "drops"],
        "handle_cut_offense": ["catches", "drops"],
        "swing_throw_offense": ["completions", "throwaways", "stalls", "hockey_assists", "callahans_thrown"],
        "under_throw_offense": ["completions", "throwaways", "stalls", "assists"],
        "short_huck_throw_offense": ["hucks_completed", "yards_thrown", "throwaways", "assists", "pulls"],
        "deep_huck_throw_offense": ["hucks_completed", "yards_thrown", "throwaways", "assists", "pulls"],
    }

    ufa_stats = list(UFAPlayerStatsYear.objects.select_related("player"))
    player_map = {p.ufa_player_id: p for p in Player.objects.exclude(ufa_player=None)}
    player_scores = defaultdict(dict)

    for skill_field, stat_fields in skill_map.items():
        raw_scores = []
        player_ids = []

        for stat in ufa_stats:
            total = 0
            for field in stat_fields:
                value = getattr(stat, field, 0)
                if "drop" in field or "throwaway" in field or "stalls" in field or "callahans_thrown" in field:
                    total -= value
                else:
                    total += value

            raw_scores.append(total)
            player_ids.append(stat.player.id)

        normed_scores = [curved_normalize(score, raw_scores) for score in raw_scores]

        for pid, score in zip(player_ids, normed_scores):
            if pid in player_map:
                player_scores[pid][skill_field] = score

    players_to_update = []
    for player in Player.objects.filter(id__in=player_scores.keys()):
        for field, val in player_scores[player.id].items():
            setattr(player, field, val)
        player.calculate_all_overall_ratings()
        players_to_update.append(player)

    if players_to_update:
        update_fields = list(skill_map.keys()) + [
            'overall_rating',
            'overall_handle_offense_rating',
            'overall_handle_defense_rating',
            'overall_cutter_offense_rating',
            'overall_cutter_defense_rating',
        ]
        Player.objects.bulk_update(players_to_update, update_fields)

    return len(players_to_update), list(skill_map.keys())


def convert_all_ufa_stats_to_players(modeladmin, request, queryset):
    all_stats = list(UFAPlayerStatsYear.objects.select_related("player"))

    for stat in all_stats:
        p = stat.player

        # Only create the Player and base info — no skill stats here
        player, created = Player.objects.update_or_create(
            ufa_player=p,
            first_name=p.first_name,
            last_name=p.last_name,
            defaults={
                "jersey_number": random.randint(0, 99),
                "height_in_inches": random.randint(66, 76),
                "weight_in_lbs": random.randint(150, 210),
                "speed": curved_normalize(
                    stat.yards_received + stat.yards_thrown,
                    [s.yards_received + s.yards_thrown for s in all_stats]
                ),
                "jumping": 75,
                "agility": 75,
            }
        )

    # After players are created, update their skill fields in bulk
    updated_count, updated_fields = bulk_update_player_skills()
    print(f"Updated {updated_count} players with skill ratings: {list(updated_fields)}")


@admin.register(UFATeam)
class UFATeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'city', 'name', 'abbreviation']
    search_fields = ['full_name', 'city']
    actions = [fetch_and_update_teams, update_team_lines, create_teams_from_ufa_teams]


@admin.register(UFAPlayer)
class UFAPlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "id")
    search_fields = ['first_name', 'last_name']
    actions = [fetch_and_update_players, convert_all_ufa_stats_to_players]


@admin.register(UFADivision)
class UFADivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(UFAPlayerTeam)
class UFAPlayerTeamAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'year', 'jersey_number', 'active')
    list_filter = ('year', 'active', 'team')
    search_fields = ('player__full_name', 'team__name', 'jersey_number')


@admin.register(UFAGame)
class UFAGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'away_team', 'home_team', 'away_score', 'home_score', 'status', 'start_timestamp')
    list_filter = ('away_team', 'home_team', 'start_timestamp')
    search_fields = ('home_team__name', 'away_team__name')
    actions = [fetch_and_update_games]


@admin.register(UFAPlayerStatsYear)
class UFAPlayerStatsYearAdmin(admin.ModelAdmin):
    list_display = ('player', 'year', 'goals', 'assists', 'blocks', 'yards_received', 'yards_thrown', 'hucks_attempted',
                    'hucks_completed', 'pulls', 'completions', 'throw_attempts', 'throwaways', 'drops',
                    'hockey_assists', 'catches', 'drops')
    list_filter = ('player', 'year')
    search_fields = ('player__first_name', 'player__last_name')
    autocomplete_fields = ('player',)
    actions = [fetch_and_update_year_stats]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'jersey_number',
        'deep_huck_cut_offense', 'deep_huck_throw_offense',
        'under_cut_offense', 'under_throw_offense',
        'handle_mark_defense', 'overall_rating',
    )
    list_filter = ('primary_line', 'primary_position', 'is_public')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    actions = [convert_all_ufa_stats_to_players]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('location', 'mascot', 'overall_rating', 'is_public')
    search_fields = ('location', 'mascot')
    list_filter = ('is_public',)
    filter_horizontal = (
        'players', 'o_line_players', 'd_line_players',
        'o_line_handlers', 'd_line_handlers',
        'o_line_cutters', 'd_line_cutters',
        'o_line_hybrids', 'd_line_hybrids',
        'bench_players'
    )
    actions = [create_teams_from_ufa_teams, update_team_lines]


@admin.register(UFASeason)
class UFASeasonAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'year', 'number_of_teams',
    )
    list_filter = ('year',)
    search_fields = ('name',)
    actions = [setup_ufa_season]


@admin.register(UFASeasonTeam)
class UFASeasonTeamAdmin(admin.ModelAdmin):
    list_display = (
        'team', 'season', 'division',
    )
    list_filter = ('team', 'season', 'division')
    search_fields = ('team',)


@admin.action(description="Setup All UFA Simulation Data")
def setup_simulation_environment(modeladmin, request, queryset):
    fetch_and_update_teams(modeladmin, request, queryset)
    fetch_and_update_players(modeladmin, request, queryset)
    fetch_and_update_games(modeladmin, request, queryset)
    fetch_and_update_year_stats(modeladmin, request, queryset)
    convert_all_ufa_stats_to_players(modeladmin, request, queryset)
    create_teams_from_ufa_teams(modeladmin, request, queryset)
    update_team_lines(modeladmin, request, queryset)
    setup_ufa_season(modeladmin, request, queryset)

    messages.success(request, "UFA simulation environment set up successfully.")


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


UserAdmin.actions = list(getattr(UserAdmin, 'actions', [])) + [setup_simulation_environment]
UserAdmin.inlines = (ProfileInline,)
