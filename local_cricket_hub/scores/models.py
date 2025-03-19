from django.db import models
from tournaments.models import Match
from teams.models import Player

class Score(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='scores')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    bowled_by = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='wickets')
    strike_rate = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if self.balls > 0:
            self.strike_rate = (self.runs / self.balls) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player.name} - {self.runs} runs"