from dataclasses import fields
from django import forms
from .models import Tournament, Match
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
        
class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['tournament','team1', 'team2', 'date', 'time', 'venue', 'is_completed', 'winner', 'mom']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }