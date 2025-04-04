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
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    gap_days = models.IntegerField(default=0)
    venues = models.TextField(help_text="Enter venue names separated by commas (e.g., Mumbai, Chennai, Mohali)",null=True, blank=True)
    tournament_winner = models.CharField(Team, null=True, blank=True,max_length=50)
    
    def __str__(self):
        return f"{self.name} ({self.club.name})"

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    team1 = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='matches_as_team1')
    team2 = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='matches_as_team2')
    date = models.DateField()
    venue = models.CharField(max_length=100)
    time = models.TimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    winner = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')
    mom = models.ForeignKey('teams.Player', on_delete=models.SET_NULL, null=True, blank=True, related_name='mom_awards')

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} - {self.date} - {self.venue}"