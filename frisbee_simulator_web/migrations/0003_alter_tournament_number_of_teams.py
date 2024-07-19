# Generated by Django 4.2.7 on 2024-01-30 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee_simulator_web', '0002_tournament_bracket_play_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='number_of_teams',
            field=models.PositiveIntegerField(choices=[(4, '4'), (8, '8')], default=4),
        ),
    ]
