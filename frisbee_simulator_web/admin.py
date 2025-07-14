import time

import requests
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
import numpy as np
import random

from .models import *
from django.db import transaction

UFA_API_BASE = "https://api.theaudl.com/api/v1"


def fetch_and_update_players(modeladmin, request, queryset):
    """Fetch and update a Player from the API using their ufa_id."""
    url = "https://www.backend.ufastats.com/api/v1/players"
    params = {'years': '2024'}
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
                                                                                          is_active=True,
                                                                                          defaults={
                                                                                              "year": api_team['year'],
                                                                                              "jersey_number": api_team[
                                                                                                  "jerseyNumber"]})

    except Exception as e:
        messages.error(request, f"Error fetching players: {str(e)}")


@admin.action(description="Fetch and Update Teams")
def fetch_and_update_teams(modeladmin, request, queryset):
    url = "https://www.backend.ufastats.com/api/v1/teams"

    params = {'years': '2024'}
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
    params = {'date': '2024-01-01:2024-12-31'}
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
    YEAR = 2024
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
    ufa_teams = UFATeam.objects.filter(year=2024)

    for ufa_team in ufa_teams:
        team, created = Team.objects.update_or_create(
            location=ufa_team.city,
            mascot=ufa_team.name,
            type="UFA",
            is_public=True,
            year=ufa_team.year
        )

        # Get UFA players on that team
        ufa_player_ids = UFAPlayerTeam.objects.filter(
            team=ufa_team,
            year=2024,
            active=True
        ).values_list('player__first_name', 'player__last_name')

        # Match to Player instances by name
        matched_players = Player.objects.filter(
            first_name__in=[p[0] for p in ufa_player_ids],
            last_name__in=[p[1] for p in ufa_player_ids]
        )
        # Assign to the team
        team.players.set(matched_players)
        team.save()


def setup_2024_ufa_season(modeladmin, request, queryset):
    ufa_teams = UFATeam.objects.filter(year=2024)
    season, created = UFASeason.objects.update_or_create(name='2024 Season', year=2024, number_of_teams=24)

    for ufa_team in ufa_teams:
        api_team = Team.objects.get(year=2024, location=ufa_team.city, mascot=ufa_team.name)
        team, created = UFASeasonTeam.objects.update_or_create(
            team=api_team,
            season=season,
            division=ufa_team.division,
        )


def assign_primary_lines_for_team(team):
    players = list(team.players.all())

    # Score players
    scored_players = []
    for p in players:
        offense_score = p.overall_handle_offense_rating + p.overall_cutter_offense_rating
        defense_score = p.overall_handle_defense_rating + p.overall_cutter_defense_rating
        scored_players.append((p, offense_score, defense_score))

    # Sort by offense score and pick top 7
    offense_line = sorted(scored_players, key=lambda x: x[1], reverse=True)[:7]
    offense_players = {p[0] for p in offense_line}

    # Sort by defense score, skip those already in offense
    remaining_for_defense = [x for x in scored_players if x[0] not in offense_players]
    defense_line = sorted(remaining_for_defense, key=lambda x: x[2], reverse=True)[:7]
    defense_players = {p[0] for p in defense_line}

    remaining_for_bench = [x for x in scored_players if x[0] not in [offense_players, remaining_for_defense]]
    bench_line = sorted(remaining_for_bench, key=lambda x: x[2], reverse=True)[:7]
    bench_players = {p[0] for p in bench_line}

    # Remaining players → bench (best remaining overall)
    used_players = offense_players.union(defense_players).union(bench_players)
    remaining = [x for x in scored_players if x[0] not in used_players]
    deep_bench_line = sorted(remaining, key=lambda x: x[1] + x[2], reverse=True)[:7]
    deep_bench_players = {p[0] for p in deep_bench_line}

    team.o_line_players.set(offense_players)
    team.d_line_players.set(defense_players)
    team.bench_players.set(bench_players)
    team.deep_bench_players.set(deep_bench_players)

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

    # Assign and save
    updates = []
    for p, *_ in scored_players:
        if p in offense_players:
            p.primary_line = 'OFFENSE'
            p.primary_position = 'OFFENSE'
        elif p in defense_players:
            p.primary_line = 'DEFENSE'
            p.primary_position = 'DEFENSE'
        elif p in bench_players:
            p.primary_line = 'BENCH'
            p.primary_position = 'DEFENSE'
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


def curved_normalize(val, all_vals, mean=75, std=10, min_score=55, max_score=95):
    mu = np.mean(all_vals)
    sigma = np.std(all_vals) or 1
    z = (val - mu) / sigma
    score = mean + z * std
    return int(max(min(score, max_score), min_score))


def bulk_update_player_skills():
    # 🧠 Define your skill logic here
    skill_map = {
        "deep_huck_cut_defense": ["blocks", "d_opportunity_stops", "d_points_played"],
        "short_huck_cut_defense": ["blocks", "d_opportunity_stops", "d_points_played"],
        "under_cut_defense": ["blocks", "d_opportunity_stops", "d_points_played"],
        "handle_mark_defense": ["blocks", "d_opportunity_stops", "d_points_played"],
        "handle_cut_defense": ["blocks", "d_opportunity_stops", "d_points_played"],

        "deep_huck_cut_offense": ["yards_received", "goals", "catches", "drops"],
        "short_huck_cut_offense": ["yards_received", "goals", "catches", "drops"],
        "under_cut_offense": ["catches", "yards_received", "goals", "drops"],
        "handle_cut_offense": ["catches", "drops"],

        "swing_throw_offense": ["completions", "throwaways", "stalls", "hockey_assists", "callahans_thrown"],
        "under_throw_offense": ["completions", "throwaways", "stalls", "assists"],
        "short_huck_throw_offense": ["hucks_attempted", "hucks_completed", "throwaways", "assists", "pulls"],
        "deep_huck_throw_offense": ["hucks_attempted", "hucks_completed", "throwaways", "assists", "pulls"],
    }

    ufa_stats = list(UFAPlayerStatsYear.objects.select_related("player"))
    player_map = {
        (p.first_name, p.last_name): p for p in Player.objects.all()
    }

    # Prepare mapping: (name) → skill → score
    player_scores = {}

    for skill_field, stat_fields in skill_map.items():
        # Extract data matrix
        data = np.array([
            [getattr(p, f, 0) for f in stat_fields] for p in ufa_stats
        ])
        # Variance-based weighting
        variances = np.var(data, axis=0)
        total_var = np.sum(variances)
        weights = variances / total_var if total_var else np.ones(len(stat_fields)) / len(stat_fields)
        weights_dict = dict(zip(stat_fields, weights))

        # Negate fields that penalize (basic rule: if "drop", "throwaway", etc.)
        for stat in stat_fields:
            if "drop" in stat or "throwaway" in stat or "stalls" in stat or "callahans_thrown" in stat:
                weights_dict[stat] *= -1

        # Score and normalize
        raw_scores = [
            sum(getattr(p, s, 0) * weights_dict[s] for s in stat_fields)
            for p in ufa_stats
        ]
        norm_scores = [
            curved_normalize(score, raw_scores) for score in raw_scores
        ]

        # Store in per-player dictionary
        for ufa_stat, score in zip(ufa_stats, norm_scores):
            key = (ufa_stat.player.first_name, ufa_stat.player.last_name)
            if key not in player_scores:
                player_scores[key] = {}
            player_scores[key][skill_field] = score

    # Apply scores to players and bulk update
    players_to_update = []
    for key, scores in player_scores.items():
        player = player_map.get(key)
        if player:
            for field, value in scores.items():
                setattr(player, field, value)

            player.calculate_all_overall_ratings()
            players_to_update.append(player)

    # Update all at once
    if players_to_update:
        all_fields = list(skill_map.keys()) + [
            'overall_rating',
            'overall_handle_offense_rating',
            'overall_handle_defense_rating',
            'overall_cutter_offense_rating',
            'overall_cutter_defense_rating'
        ]
        Player.objects.bulk_update(players_to_update, all_fields)

    return len(players_to_update), skill_map.keys()


def convert_all_ufa_stats_to_players(modeladmin, request, queryset):
    all_stats = list(UFAPlayerStatsYear.objects.select_related("player"))

    for stat in all_stats:
        p = stat.player

        # Only create the Player and base info — no skill stats here
        player, created = Player.objects.update_or_create(
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
    actions = [setup_2024_ufa_season]


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

    messages.success(request, "UFA simulation environment set up successfully.")


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


UserAdmin.actions = list(getattr(UserAdmin, 'actions', [])) + [setup_simulation_environment]
UserAdmin.inlines = (ProfileInline,)
