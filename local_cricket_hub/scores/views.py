from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from tournaments.models import Match
from scores.models import Inning, BattingScore, BowlingScore

@login_required
def match_dashboard(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    innings = match.innings.all().order_by('id')

    fall_of_wickets = {}
    for inning in innings:
        wickets = []
        current_runs = 0
        for score in inning.batting_scores.filter(is_out=True).order_by('id'):
            current_runs += score.runs
            wickets.append(f"{current_runs}-{inning.batting_scores.filter(is_out=True, id__lte=score.id).count()} ({score.player.name})")
        fall_of_wickets[inning.id] = wickets

    context = {
        'match': match,
        'innings': innings,
        'team1': match.team1,
        'team2': match.team2,
        'tournament': match.tournament,
        'fall_of_wickets': fall_of_wickets,
    }

    if innings.exists():
        context['inning1'] = innings[0]
        context['inning1_batting'] = innings[0].batting_scores.all().order_by('-runs')
        context['inning1_bowling'] = innings[0].bowling_scores.all().order_by('-wickets')
        
        if len(innings) > 1:
            context['inning2'] = innings[1]
            context['inning2_batting'] = innings[1].batting_scores.all().order_by('-runs')
            context['inning2_bowling'] = innings[1].bowling_scores.all().order_by('-wickets')

    return render(request, 'match_dashboard.html', context)