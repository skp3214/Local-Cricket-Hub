from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tournament, Match
from .forms import TournamentForm, FixtureForm, MatchForm
from datetime import timedelta
from datetime import time,datetime
from django.http import HttpResponseForbidden
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Tournament, Match
from scores.models import BattingScore, BowlingScore
from django.db.models import Sum

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
def edit_tournament(request,tournament_id):  
    tournament = get_object_or_404(Tournament, id=tournament_id, club__owner=request.user)
    
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect('tournaments:tournament_detail', tournament_id=tournament.id)
    else:
        form = TournamentForm(instance=tournament)
    return render(request, 'create_tournament.html', {'form': form,'edit':True})

@login_required
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    teams = tournament.teams.all()
    current_time = timezone.now()
    upcoming_matches = tournament.matches.filter(date__gt=current_time)
    past_matches = tournament.matches.filter(date__lt=current_time)
    today_matches = tournament.matches.filter(date=current_time)

    points_table = []
    for team in teams:
        matches_played = tournament.matches.filter(team1=team) | tournament.matches.filter(team2=team)
        gp = matches_played.count()  
        wins = 0
        losses = 0
        
        total_batting_rr = 0.0
        total_bowling_rr = 0.0
        matches_counted = 0

        for match in matches_played:
            inning_team1 = match.innings.filter(team=match.team1).first()
            inning_team2 = match.innings.filter(team=match.team2).first()

            if match.winner == team:
                wins += 1
            elif match.winner and match.winner != team:
                losses += 1

            batted = False
            bowled = False

            if inning_team1 and inning_team1.team == team:
                runs = inning_team1.total_runs
                overs = inning_team1.overs or 0.1
                total_batting_rr += runs / overs
                batted = True
            if inning_team2 and inning_team2.team == team:
                runs = inning_team2.total_runs
                overs = inning_team2.overs or 0.1
                total_batting_rr += runs / overs
                batted = True

            if inning_team1 and inning_team1.team != team:
                runs = inning_team1.total_runs
                overs = inning_team1.overs or 0.1
                total_bowling_rr += runs / overs
                bowled = True
            if inning_team2 and inning_team2.team != team:
                runs = inning_team2.total_runs
                overs = inning_team2.overs or 0.1
                total_bowling_rr += runs / overs
                bowled = True

            if batted or bowled:
                matches_counted += 1

        pts = wins * 2  
        
        if matches_counted > 0:
            avg_batting_rr = total_batting_rr / matches_counted
            avg_bowling_rr = total_bowling_rr / matches_counted
            nrr = avg_batting_rr - avg_bowling_rr
        else:
            nrr = 0.0

        points_table.append({
            'team': team,
            'pts': pts,
            'gp': gp,
            'w': wins,
            'l': losses,
            'nrr': round(nrr, 3)  
        })

    points_table.sort(key=lambda x: (-x['pts'], -x['nrr']))

    for i, entry in enumerate(points_table, 1):
        entry['rank'] = i

    batting_scores = BattingScore.objects.filter(inning__match__tournament=tournament).order_by('-runs')
    top_batsmen = []
    seen_players = set()
    for score in batting_scores:
        if score.player not in seen_players and len(top_batsmen) < 5:
            player_total_runs = BattingScore.objects.filter(player=score.player, inning__match__tournament=tournament).aggregate(total_runs=Sum('runs'))['total_runs'] or 0
            top_batsmen.append({
                'player': score.player,
                'highest_score': score.runs,
                'total_runs': player_total_runs
            })
            seen_players.add(score.player)

    bowling_scores = BowlingScore.objects.filter(inning__match__tournament=tournament).order_by('-wickets')
    top_bowlers = []
    seen_players = set()
    for score in bowling_scores:
        if score.player not in seen_players and len(top_bowlers) < 5:
            player_total_wickets = BowlingScore.objects.filter(player=score.player, inning__match__tournament=tournament).aggregate(total_wickets=Sum('wickets'))['total_wickets'] or 0
            player_total_runs = BowlingScore.objects.filter(player=score.player, inning__match__tournament=tournament).aggregate(total_runs=Sum('runs'))['total_runs'] or 0
            player_total_overs = BowlingScore.objects.filter(player=score.player, inning__match__tournament=tournament).aggregate(total_overs=Sum('overs'))['total_overs'] or 0.1
            economy = player_total_runs / player_total_overs if player_total_overs else 0
            top_bowlers.append({
                'player': score.player,
                'total_wickets': player_total_wickets,
                'economy': round(economy, 2)
            })
            seen_players.add(score.player)

    return render(request, 'tournament_detail.html', {
        'tournament': tournament,
        'teams': teams,
        'upcoming_matches': upcoming_matches,
        'past_matches': past_matches,
        'todays_matches': today_matches,
        'points_table': points_table,
        'top_batsmen': top_batsmen,
        'top_bowlers': top_bowlers,
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

            start_date = tournament.start_date
            end_date = tournament.end_date
            gap_days = tournament.gap_days
            venues = [venue.strip() for venue in tournament.venues.split(',')] 
            teams = list(tournament.teams.all())

            match_pairs = []
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    match_pairs.append((teams[i], teams[j]))  
                    match_pairs.append((teams[j], teams[i]))  

            total_matches = len(match_pairs)
            print(f"Total matches to schedule: {total_matches}")

            total_days = (end_date - start_date).days + 1  
            max_match_days = total_days // (gap_days + 1)  
            matches_per_day = max(1, (total_matches + max_match_days - 1) // max_match_days)  

            print(f"Total days: {total_days}, Max match days with gap: {max_match_days}, Matches per day: {matches_per_day}")

            current_date = start_date
            match_count = 0
            venue_index = 0

            while match_count < total_matches and current_date <= end_date:
                teams_playing_today = set()
                matches_scheduled_today = 0
                match_time = time(10, 0)  
                while (match_count < total_matches and 
                       matches_scheduled_today < matches_per_day and 
                       match_time <= time(20, 0)):  
                    team1, team2 = match_pairs[match_count]

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

                        teams_playing_today.add(team1)
                        teams_playing_today.add(team2)

                        match_time = (datetime.combine(current_date, match_time) + timedelta(hours=2)).time()

                current_date += timedelta(days=gap_days + 1 if matches_scheduled_today > 0 else 1)

            return redirect('tournaments:tournament_detail', tournament_id=tournament.id)
        else:
            print("Form is invalid. Errors:", form.errors)
    else:
        form = FixtureForm(instance=tournament)
    return render(request, 'create_fixture.html', {'form': form, 'tournament': tournament})


@login_required
def add_match(request):
    
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save()
            
            return redirect('scores:match_dashboard', match_id=match.id)
    else:
        form = MatchForm()
    return render(request, 'add_match.html', {'form': form})

@login_required
def edit_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if match.tournament.club.owner != request.user:
        return redirect('scores:match_dashboard', match_id=match_id)
    
    if match.date != date.today():
        return redirect('scores:match_dashboard', match_id=match_id)

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('scores:match_dashboard', match_id=match.id)
    else:
        form = MatchForm(instance=match)
    return render(request, 'edit_match.html', {'form': form, 'match': match})