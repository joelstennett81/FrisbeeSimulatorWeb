# Generated by Django 4.2.7 on 2024-04-29 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee_simulator_web', '0021_rename_prequarter_final_round_completed_tournament_pre_quarterfinal_round_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='pool_play_seeds_set',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournament',
            name='set_pool_play_seeds_manually',
            field=models.BooleanField(default=False),
        ),
    ]
