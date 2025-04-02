from django.db import models
from tournaments.models import Match
from teams.models import Player

class Inning(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='innings')
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    total_runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    overs = models.FloatField(default=0.0)
    extras = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team.name} - {self.total_runs}/{self.wickets} in {self.overs} overs"
    
class BattingScore(models.Model):
    inning = models.ForeignKey(Inning, on_delete=models.CASCADE, related_name='batting_scores')
    player = models.ForeignKey('teams.Player', on_delete=models.CASCADE)
    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    is_out = models.BooleanField(default=False)
    out_type = models.CharField(max_length=50, blank=True, null=True)
    bowled_by = models.ForeignKey('teams.Player', on_delete=models.SET_NULL, null=True, blank=True, related_name='wickets_taken')
    caught_by = models.ForeignKey('teams.Player', on_delete=models.SET_NULL, null=True, blank=True, related_name='catches')

    @property
    def strike_rate(self):
        return round((self.runs / self.balls) * 100, 2) if self.balls > 0 else 0

    def __str__(self):
        return f"{self.player.name} - {self.runs} ({self.balls})"

class BowlingScore(models.Model):
    inning = models.ForeignKey(Inning, on_delete=models.CASCADE, related_name='bowling_scores')
    player = models.ForeignKey('teams.Player', on_delete=models.CASCADE)
    overs = models.FloatField(default=0)
    maidens = models.IntegerField(default=0)
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    wides = models.IntegerField(default=0)
    noballs = models.IntegerField(default=0)

    @property
    def economy(self):
        return round(self.runs / self.overs, 2) if self.overs > 0 else 0

    def __str__(self):
        return f"{self.player.name} - {self.wickets}/{self.runs} in {self.overs} overs"
