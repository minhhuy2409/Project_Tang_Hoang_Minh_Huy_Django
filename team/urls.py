from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.player_profile, name='player_profile'),
    path('schedule/', views.match_schedule, name='match_schedule'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('attendance/', views.register_attendance, name='register_attendance'),
    path('attendance/', views.register_attendance, name='register_attendance'),
    path('stats/', views.player_stats, name='player_stats'),
    path('stats/', views.player_stats, name='player_stats'),
    path('signup/', views.signup, name='signup'),
    path('', views.landing, name='landing'),
]
