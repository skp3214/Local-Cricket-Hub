from django import forms
from .models import BattingScore, BowlingScore, Inning

class BattingScoreForm(forms.ModelForm):
    class Meta:
        model = BattingScore
        fields = ['runs', 'balls', 'fours', 'sixes', 'is_out', 'out_type']
        widgets = {
            'out_type': forms.TextInput(attrs={'placeholder': 'e.g., c Player b Player'}),
        }

class BowlingScoreForm(forms.ModelForm):
    class Meta:
        model = BowlingScore
        fields = ['overs', 'maidens', 'runs', 'wickets', 'wides', 'noballs']

class InningForm(forms.ModelForm):
    class Meta:
        model = Inning
        fields = ['total_runs', 'wickets', 'overs', 'extras']