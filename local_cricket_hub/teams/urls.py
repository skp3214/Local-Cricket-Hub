from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('register/', views.register_team, name='register_team'),
    path('<int:team_id>/', views.team_dashboard, name='team_dashboard'),
    path('<int:team_id>/add_player/', views.add_player, name='add_player'),
    path('<int:team_id>/associate_club/', views.associate_club, name='associate_club'),
    path('filter_clubs_by_pincode/', views.filter_clubs_by_pincode, name='filter_clubs_by_pincode'),
    path('<int:team_id>/participate/<int:tournament_id>/', views.participate_tournament, name='participate_tournament'),
    path('<int:team_id>/edit_player/<int:player_id>/', views.edit_player, name='edit_player'),
]