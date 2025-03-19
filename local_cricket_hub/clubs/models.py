from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CricketClub(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='club_images/', blank=True, null=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clubs')

    def clean(self):
        # Check if the owner already owns a team
        if self.owner.teams.exists():
            raise ValidationError("A user who owns a team cannot create a club.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving
        super().save(*args, **kwargs)

    def __personally__(self):
        return self.name