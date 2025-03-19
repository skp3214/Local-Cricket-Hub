from django.db import models
from django.contrib.auth.models import User
from clubs.models import CricketClub

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')
    club = models.ForeignKey(CricketClub, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name

class Player(models.Model):
    PLAYER_TYPES = (
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('allrounder', 'Allrounder'),
    )
    DESIGNATIONS = (
        ('captain', 'Captain'),
        ('vc', 'Vice-Captain'),
        ('wk', 'Wicket-Keeper'),
        ('normal', 'Normal Player'),
    )
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    player_type = models.CharField(max_length=10, choices=PLAYER_TYPES)
    designation = models.CharField(max_length=10, choices=DESIGNATIONS)

    def __str__(self):
        return f"{self.name} ({self.team.name})"