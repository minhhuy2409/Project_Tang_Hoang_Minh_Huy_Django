from django.contrib import admin
from .models import UserProfile, Player, Match, Attendance, GoalEvent, AssistEvent

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'shirt_number', 'position', 'user_profile')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('opponent', 'datetime', 'location', 'score')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'status')
    list_filter = ('status',)

@admin.register(GoalEvent)
class GoalEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'minute')

@admin.register(AssistEvent)
class AssistEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'minute')
