# Generated by Django 4.2.7 on 2024-02-03 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee_simulator_web', '0006_tournament_bracket_games_tournament_pool_play_games'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='bracket_games',
        ),
        migrations.AddField(
            model_name='tournament',
            name='final_round_games',
            field=models.ManyToManyField(related_name='final_games_tournament', to='frisbee_simulator_web.game'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='semifinal_round_games',
            field=models.ManyToManyField(related_name='semifinal_games_tournament', to='frisbee_simulator_web.game'),
        ),
    ]
