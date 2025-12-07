from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Avg, Count
from .models import GoalEvent, AssistEvent, Attendance, Player

def update_player_stats(player):
    # Update goals
    total_goals = GoalEvent.objects.filter(player=player).count()
    player.goals = total_goals

    # Update assists
    total_assists = AssistEvent.objects.filter(player=player).count()
    player.assists = total_assists

    # Update matches played (only count if status is 'going')
    matches_played = Attendance.objects.filter(player=player, status='going').count()
    player.matches_played = matches_played

    # Update average rating
    avg_rating = Attendance.objects.filter(player=player, rating__isnull=False).aggregate(Avg('rating'))['rating__avg']
    player.average_rating = avg_rating if avg_rating else 0.0

    player.save()

@receiver(post_save, sender=GoalEvent)
@receiver(post_delete, sender=GoalEvent)
def update_goals(sender, instance, **kwargs):
    update_player_stats(instance.player)

@receiver(post_save, sender=AssistEvent)
@receiver(post_delete, sender=AssistEvent)
def update_assists(sender, instance, **kwargs):
    update_player_stats(instance.player)

@receiver(post_save, sender=Attendance)
@receiver(post_delete, sender=Attendance)
def update_attendance_stats(sender, instance, **kwargs):
    update_player_stats(instance.player)
