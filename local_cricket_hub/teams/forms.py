from django import forms
from .models import Team, Player

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'image'] 

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'player_type', 'designation']