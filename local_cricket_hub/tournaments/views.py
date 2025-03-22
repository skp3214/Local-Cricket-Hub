from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tournament, Match
from .forms import TournamentForm, FixtureForm
from datetime import timedelta
from datetime import time,datetime

@login_required
def create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.club = request.user.clubs.first()
            tournament.save()
            return redirect('tournaments:tournament_detail', tournament_id=tournament.id)
    else:
        form = TournamentForm()
    return render(request, 'create_tournament.html', {'form': form})

@login_required
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    teams = tournament.teams.all()
    upcoming_matches = tournament.matches.filter(date__gte=datetime.now())
    past_matches = tournament.matches.filter(date__lt=datetime.now())
    
    return render(request, 'tournament_detail.html', {
        'tournament': tournament,
        'teams': teams,
        'upcoming_matches': upcoming_matches,
        'past_matches': past_matches,
        'user': request.user
    })
    

@login_required
def create_fixture(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, club__owner=request.user)
    if request.method == 'POST':
        form = FixtureForm(request.POST, instance=tournament)
        if form.is_valid():
            tournament = form.save()
            print("Form is valid. Saving tournament and generating fixtures...")

            # Generate fixtures
            start_date = tournament.start_date
            end_date = tournament.end_date
            gap_days = tournament.gap_days
            venues = [venue.strip() for venue in tournament.venues.split(',')]  # Split comma-separated string
            teams = list(tournament.teams.all())

            # Generate all possible match pairs (each team plays twice with every other team)
            match_pairs = []
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    match_pairs.append((teams[i], teams[j]))  # First match
                    match_pairs.append((teams[j], teams[i]))  # Second match (reverse fixture)

            total_matches = len(match_pairs)
            print(f"Total matches to schedule: {total_matches}")

            # Calculate available days between start_date and end_date
            total_days = (end_date - start_date).days + 1  # Inclusive of start and end date
            max_match_days = total_days // (gap_days + 1)  # Number of days available with gap
            matches_per_day = max(1, (total_matches + max_match_days - 1) // max_match_days)  # Ceiling division

            print(f"Total days: {total_days}, Max match days with gap: {max_match_days}, Matches per day: {matches_per_day}")

            current_date = start_date
            match_count = 0
            venue_index = 0

            # Schedule matches
            while match_count < total_matches and current_date <= end_date:
                teams_playing_today = set()
                matches_scheduled_today = 0
                match_time = time(10, 0)  # Start at 10:00 AM

                # Schedule up to `matches_per_day` matches on the current day
                while (match_count < total_matches and 
                       matches_scheduled_today < matches_per_day and 
                       match_time <= time(20, 0)):  # Stop at 8:00 PM
                    team1, team2 = match_pairs[match_count]

                    # Ensure neither team is already playing today
                    if team1 not in teams_playing_today and team2 not in teams_playing_today:
                        Match.objects.create(
                            tournament=tournament,
                            team1=team1,
                            team2=team2,
                            date=current_date,
                            venue=venues[venue_index % len(venues)],
                            time=match_time
                        )
                        match_count += 1
                        matches_scheduled_today += 1
                        venue_index += 1

                        # Add teams to today's playing set
                        teams_playing_today.add(team1)
                        teams_playing_today.add(team2)

                        # Increment match time by 2 hours
                        match_time = (datetime.combine(current_date, match_time) + timedelta(hours=2)).time()

                # Move to the next match day with gap
                current_date += timedelta(days=gap_days + 1 if matches_scheduled_today > 0 else 1)

            return redirect('tournaments:tournament_detail', tournament_id=tournament.id)
        else:
            print("Form is invalid. Errors:", form.errors)
    else:
        form = FixtureForm(instance=tournament)
    return render(request, 'create_fixture.html', {'form': form, 'tournament': tournament})