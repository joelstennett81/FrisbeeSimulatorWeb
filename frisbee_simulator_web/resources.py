# resources.py
from import_export import resources
from .models import Player, Team


class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player
        import_id_fields = ['first_name', 'last_name']
        fields = ('first_name', 'last_name', 'jersey_number', 'height_in_inches', 'weight_in_lbs',
                  'speed', 'jumping', 'agility', 'deep_huck_cut_defense', 'short_huck_cut_defense',
                  'under_cut_defense', 'handle_mark_defense', 'handle_cut_defense', 'deep_huck_cut_offense',
                  'short_huck_cut_offense', 'under_cut_offense', 'handle_cut_offense', 'swing_throw_offense',
                  'under_throw_offense', 'short_huck_throw_offense', 'deep_huck_throw_offense', 'is_public',
                  'primary_line', 'primary_position', 'team')

    def before_import_row(self, row, **kwargs):
        # Convert team name to Team instance
        team_name = row['team']
        team, _ = Team.objects.get_or_create(location=team_name)
        row['team'] = team

    def after_save_instance(self, instance, using_transactions, dry_run):
        # Assign player to the correct line based on their primary position
        if instance.primary_line == 'OFFENSE':
            instance.team.o_line_players.add(instance)
            if instance.primary_position == 'HANDLE':
                instance.team.o_line_handlers.add(instance)
            elif instance.primary_position == 'CUTTER':
                instance.team.o_line_cutters.add(instance)
            elif instance.primary_position == 'HYBRID':
                instance.team.o_line_hybrids.add(instance)
        elif instance.primary_line == 'DEFENSE':
            instance.team.d_line_players.add(instance)
            if instance.primary_position == 'HANDLE':
                instance.team.d_line_handlers.add(instance)
            elif instance.primary_position == 'CUTTER':
                instance.team.d_line_cutters.add(instance)
            elif instance.primary_position == 'HYBRID':
                instance.team.d_line_hybrids.add(instance)
        elif instance.primary_line == 'BENCH':
            instance.team.bench_players.add(instance)

        # Add more conditions here based on other positions like 'cutters', etc.
