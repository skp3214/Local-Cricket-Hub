# Generated by Django 5.1.7 on 2025-03-19 16:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('overs', models.IntegerField(choices=[(20, '20 Overs'), (50, '50 Overs')])),
                ('team_limit', models.IntegerField(validators=[django.core.validators.MinValueValidator(2)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('gap_days', models.IntegerField(default=1)),
                ('venues', models.JSONField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournaments', to='clubs.cricketclub')),
                ('teams', models.ManyToManyField(related_name='tournaments', to='teams.team')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('venue', models.CharField(max_length=100)),
                ('is_completed', models.BooleanField(default=False)),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_team1', to='teams.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_team2', to='teams.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='tournaments.tournament')),
            ],
        ),
    ]
