from django import forms
from .models import CricketClub

class ClubForm(forms.ModelForm):
    class Meta:
        model = CricketClub
        fields = ['name', 'image', 'city', 'pincode']