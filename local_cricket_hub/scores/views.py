from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tournaments.models import Match
from teams.models import Player
from scores.models import Inning, BattingScore, BowlingScore
from .forms import BattingScoreForm, BowlingScoreForm
from django.http import HttpResponseForbidden
from datetime import date

@login_required
def match_dashboard(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    innings = match.innings.all().order_by('id')
    
    if match.date > date.today():
        if match.tournament.club.owner == request.user:
            return redirect("tournaments:tournament_detail",tournament_id = match.tournament.id)
        else:
            return redirect("teams:team_dashboard", team_id = match.team1.id if match.team1.owner == request.user else match.team2.id) 

    
    if not innings.exists():
        Inning.objects.create(match=match, team=match.team1, total_runs=0, wickets=0, overs=0.0, extras=0)
        Inning.objects.create(match=match, team=match.team2, total_runs=0, wickets=0, overs=0.0, extras=0)
        innings = match.innings.all().order_by('id')

    context = {
        'match': match,
        'innings': innings,
        'team1': match.team1.players.all(),
        'team2': match.team2.players.all(),
        'tournament': match.tournament,
    }
    
    if innings.exists():
        context['inning1'] = innings[0]
        context['inning1_batting'] = innings[0].batting_scores.all().order_by('-runs')
        context['inning1_bowling'] = innings[0].bowling_scores.all().order_by('-wickets')
        
        if len(innings) > 1:
            context['inning2'] = innings[1]
            context['inning2_batting'] = innings[1].batting_scores.all().order_by('-runs')
            context['inning2_bowling'] = innings[1].bowling_scores.all().order_by('-wickets')
            
            if match.winner:
                if match.winner == innings[0].team:
                    context['win_margin'] = innings[0].total_runs - innings[1].total_runs
                    context['win_by'] = 'runs'
                else:
                    context['win_margin'] = 10 - innings[1].wickets
                    context['win_by'] = 'wickets'
    
    if match.mom:
        mom_batting = BattingScore.objects.filter(player=match.mom, inning__match=match).first()
        context['mom_batting'] = mom_batting
    
    return render(request, 'match_dashboard.html', context)


@login_required
def edit_batting_score(request, match_id, player_id):
    match = get_object_or_404(Match, id=match_id)
    player = get_object_or_404(Player, id=player_id)
    
    if match.tournament.club.owner != request.user:
        return redirect('scores:match_dashboard', match_id=match_id)
    
    if match.date != date.today():
        return redirect('scores:match_dashboard', match_id=match_id)

    innings = match.innings.all().order_by('id')

    inning = None
    for i in innings:
        if i.team == player.team:
            inning = i
            break

    if not inning:
        return redirect('scores:match_dashboard', match_id=match_id)

    batting_score, created = BattingScore.objects.get_or_create(
        inning=inning,
        player=player,
        defaults={'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 'is_out': False}
    )

    if request.method == 'POST':
        form = BattingScoreForm(request.POST, instance=batting_score)
        if form.is_valid():
            form.save()
            messages.success(request, f"Batting score for {player.name} updated successfully!")
            return redirect('scores:match_dashboard', match_id=match_id)
    else:
        form = BattingScoreForm(instance=batting_score)

    return render(request, 'edit_batting_score.html', {
        'form': form,
        'player': player,
        'match': match,
        'inning': inning,
    })

@login_required
def edit_bowling_score(request, match_id, player_id):
    match = get_object_or_404(Match, id=match_id)
    player = get_object_or_404(Player, id=player_id)
    
    if match.tournament.club.owner != request.user:
        return redirect('scores:match_dashboard', match_id=match_id)
    
    if match.date != date.today():
        return redirect('scores:match_dashboard', match_id=match_id)

    innings = match.innings.all().order_by('id')

    inning = None
    for i in innings:
        if i.team != player.team:
            inning = i
            break

    if not inning:
        return redirect('scores:match_dashboard', match_id=match_id)

    bowling_score, created = BowlingScore.objects.get_or_create(
        inning=inning,
        player=player,
        defaults={'overs': 0, 'maidens': 0, 'runs': 0, 'wickets': 0, 'wides': 0, 'noballs': 0}
    )

    if request.method == 'POST':
        form = BowlingScoreForm(request.POST, instance=bowling_score)
        if form.is_valid():
            form.save()
            messages.success(request, f"Bowling score for {player.name} updated successfully!")
            return redirect('scores:match_dashboard', match_id=match_id)
    else:
        form = BowlingScoreForm(instance=bowling_score)

    return render(request, 'edit_bowling_score.html', {
        'form': form,
        'player': player,
        'match': match,
        'inning': inning,
    })
    
@login_required
def edit_inning_scores(request, match_id, inning_id):
    match = get_object_or_404(Match, id=match_id)
    inning = get_object_or_404(Inning, id=inning_id, match=match)
    
    if match.tournament.club.owner != request.user:
        return redirect('scores:match_dashboard', match_id=match_id)
    
    if match.date != date.today():
        return redirect('scores:match_dashboard', match_id=match_id)

    if request.method == 'POST':
        inning.total_runs = int(request.POST.get('total_runs', inning.total_runs))
        inning.wickets = int(request.POST.get('wickets', inning.wickets))
        inning.overs = float(request.POST.get('overs', inning.overs))
        inning.extras = int(request.POST.get('extras', inning.extras))
        inning.save()

        return redirect('scores:match_dashboard', match_id=match_id)

    context = {
        'match': match,
        'inning': inning,
    }
    return render(request, 'edit_inning_score.html', context)