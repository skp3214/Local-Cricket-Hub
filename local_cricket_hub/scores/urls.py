# tournaments/urls.py
from django.urls import path
from . import views

app_name = 'scores'

urlpatterns = [
    path('match/<int:match_id>/', views.match_dashboard, name='match_dashboard'),
]