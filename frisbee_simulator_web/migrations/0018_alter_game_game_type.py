# Generated by Django 4.2.7 on 2024-03-27 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee_simulator_web', '0017_alter_game_game_type_alter_game_tournament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_type',
            field=models.CharField(choices=[('Pool Play', 'Pool Play'), ('Pre-Quarterfinal', 'Pre-Quarterfinal'), ('Quarterfinal', 'Quarterfinal'), ('Semifinal', 'Semifinal'), ('Championship', 'Championship'), ('3rd-Place Final', '3rd-Place Final'), ('5th-Place Semifinal', '5th-Place Semifinal'), ('5th-Place Final', '5th-Place Final'), ('7th-Place Final', '7th-Place Final'), ('9th-Place Quarterfinal', '9th-Place Quarterfinal'), ('9th-Place Semifinal', '9th-Place Semifinal'), ('9th-Place Final', '9th-Place Final'), ('11th-Place Final', '11th-Place Final'), ('13th-Place Semifinal', '13th-Place Semifinal'), ('13th-Place Final', '13th-Place Final'), ('15th-Place Final', '15th-Place Final'), ('Exhibition', 'Exhibition')], default='Exhibition', max_length=50),
        ),
    ]