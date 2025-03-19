from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CricketClub
from .forms import ClubForm
from tournaments.models import Match
import datetime

@login_required
def register_club(request):
    if request.user.teams.exists():  
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.owner = request.user
            club.save()
            return redirect('clubs:club_dashboard', club_id=club.id)
    else:
        form = ClubForm()
    return render(request, 'register_club.html', {'form': form})

@login_required
def club_dashboard(request, club_id):
    club = get_object_or_404(CricketClub, id=club_id, owner=request.user)
    teams = club.teams.all()
    tournaments = club.tournaments.all()
    today = datetime.date.today()
    today_match = Match.objects.filter(tournament__club=club, date=today, is_completed=False).first()
    return render(request, 'club_dashboard.html', {
        'club': club, 'teams': teams, 'tournaments': tournaments, 'today_match': today_match
    })