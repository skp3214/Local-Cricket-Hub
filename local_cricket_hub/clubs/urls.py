from django.urls import path
from . import views

app_name = 'clubs'

urlpatterns = [
    path('register/', views.register_club, name='register_club'),
    path('<int:club_id>/', views.club_dashboard, name='club_dashboard'),
]