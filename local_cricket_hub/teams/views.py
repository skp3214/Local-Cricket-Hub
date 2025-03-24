from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Team
from .forms import TeamForm, PlayerForm
from clubs.models import CricketClub
from tournaments.models import Tournament,Match
from datetime import datetime
from django.db.models import Q

@login_required
def register_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user
            team.save()
            return redirect('teams:team_dashboard', team_id=team.id)
    else:
        form = TeamForm()
    return render(request, 'register_team.html', {'form': form})

@login_required
def team_dashboard(request, team_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    players = team.players.all()
    tournaments_joined = team.tournaments.all()
    upcoming_matches = Match.objects.filter((Q(team1=team) | Q(team2=team)) & Q(date__gte=datetime.now()))
    past_matches = Match.objects.filter((Q(team1=team) | Q(team2=team)) & Q(date__lt=datetime.now()))
    
    
    if team.club:
        available_tournaments = team.club.tournaments.exclude(teams=team)
    else:
        available_tournaments = Tournament.objects.none()

    return render(request, 'team_dashboard.html', {
        'team': team,
        'players': players,
        'tournaments_joined': tournaments_joined,
        'available_tournaments': available_tournaments,
        'upcoming_matches': upcoming_matches,
        'past_matches': past_matches
    })

@login_required
def add_player(request, team_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    if team.players.count() >= 11:
        messages.error(request, 'Team already has 11 players.')
        return redirect('teams:team_dashboard', team_id=team.id)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.save()
            return redirect('teams:team_dashboard', team_id=team.id)
    else:
        form = PlayerForm()
    return render(request, 'add_player.html', {'form': form, 'team': team})

@login_required
def edit_player(request, team_id, player_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    player = get_object_or_404(team.players, id=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('teams:team_dashboard', team_id=team.id)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'add_player.html', {'form': form, 'team': team, 'edit': True,'player':player})


@login_required
def associate_club(request, team_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    if request.method == 'POST':
        club_id = request.POST.get('club')
        if club_id:
            club = get_object_or_404(CricketClub, id=club_id)
            team.club = club
            team.save()
            messages.success(request, f"Your team is now associated with {club.name}.")
        else:
            messages.error(request, "Please select a club.")
        return redirect('teams:team_dashboard', team_id=team.id)
    return redirect('teams:team_dashboard', team_id=team.id)

@login_required
def filter_clubs_by_pincode(request):
    if request.method == 'POST':
        pincode = request.POST.get('pincode')
        if pincode:
            clubs = CricketClub.objects.filter(pincode=pincode).values('id', 'name', 'city')
            return JsonResponse({'clubs': list(clubs)})
        return JsonResponse({'clubs': []})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def participate_tournament(request, team_id, tournament_id):
    team = get_object_or_404(Team, id=team_id, owner=request.user)
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if tournament.teams.count() < tournament.team_limit:
        tournament.teams.add(team)
        messages.success(request, f"Successfully joined {tournament.name}!")
    else:
        messages.error(request, "Cannot join. Tournament team limit surpassed.")

    return redirect('teams:team_dashboard', team_id=team.id)
