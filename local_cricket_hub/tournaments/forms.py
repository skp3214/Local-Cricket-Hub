from django import forms
from .models import Tournament
import json
class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'overs', 'team_limit']
    
class FixtureForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['start_date', 'end_date', 'gap_days', 'venues']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    