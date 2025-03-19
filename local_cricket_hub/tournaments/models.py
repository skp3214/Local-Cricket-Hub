from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from clubs.models import CricketClub
from teams.models import Team

class Tournament(models.Model):
    OVERS_CHOICES = (
        (20, '20 Overs'),
        (50, '50 Overs'),
    )
    club = models.ForeignKey(CricketClub, on_delete=models.CASCADE, related_name='tournaments')
    name = models.CharField(max_length=100)
    overs = models.IntegerField(choices=OVERS_CHOICES)
    team_limit = models.IntegerField(validators=[MinValueValidator(2)])
    teams = models.ManyToManyField(Team, related_name='tournaments')
    start_date = models.DateField()
    end_date = models.DateField()
    gap_days = models.IntegerField(default=1)
    venues = models.JSONField()  # Store list of venue names

    def __str__(self):
        return f"{self.name} ({self.club.name})"

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team2')
    date = models.DateField()
    venue = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} - {self.date}"