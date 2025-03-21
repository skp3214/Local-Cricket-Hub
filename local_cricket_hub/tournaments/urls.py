from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('create/', views.create_tournament, name='create_tournament'),
    path('<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('<int:tournament_id>/create-fixture/', views.create_fixture, name='create_fixture'),
]