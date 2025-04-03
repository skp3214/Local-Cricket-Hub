from django.urls import path
from . import views

app_name = 'scores'

urlpatterns = [
    path('match/<int:match_id>/', views.match_dashboard, name='match_dashboard'),
    path('match/<int:match_id>/edit-batting/<int:player_id>/', views.edit_batting_score, name='edit_batting_score'),
    path('match/<int:match_id>/edit-bowling/<int:player_id>/', views.edit_bowling_score, name='edit_bowling_score'),
    path('match/<int:match_id>/edit-inning/<int:inning_id>/', views.edit_inning_scores, name='edit_inning_scores'),
]