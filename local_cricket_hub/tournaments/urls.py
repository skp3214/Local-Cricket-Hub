from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('create/', views.create_tournament, name='create_tournament'),
    path('edit/<int:tournament_id>/',views.edit_tournament,name='edit_tournament'),
    path('<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('<int:tournament_id>/create-fixture/', views.create_fixture, name='create_fixture'),
    path('add-match/', views.add_match, name='add_match'),
    path('edit-match/<int:match_id>/', views.edit_match, name='edit_match'),
]