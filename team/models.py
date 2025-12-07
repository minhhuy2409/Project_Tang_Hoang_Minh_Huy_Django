from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('player', 'Player'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Player(models.Model):
    POSITION_CHOICES = (
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    )
    FOOT_CHOICES = (
        ('left', 'Left'),
        ('right', 'Right'),
        ('both', 'Both'),
    )
    STYLE_CHOICES = (
        ('keeping', 'Keeping ball'),
        ('long_pass', 'Long pass'),
        ('pressing', 'Pressing'),
        # Add more styles as needed
    )

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    shirt_number = models.PositiveIntegerField()
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    foot = models.CharField(max_length=5, choices=FOOT_CHOICES)
    playing_style = models.CharField(max_length=20, choices=STYLE_CHOICES)
    average_rating = models.FloatField(default=0)
    matches_played = models.PositiveIntegerField(default=0)
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    health_status = models.CharField(max_length=100, blank=True)  # Can be enhanced later

    def __str__(self):
        return f"{self.name} (#{self.shirt_number})"

class Match(models.Model):
    opponent = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    score = models.CharField(max_length=20, blank=True)
    tactical_notes = models.TextField(blank=True)
    players = models.ManyToManyField(Player, through='Attendance')

    def __str__(self):
        return f"Match vs {self.opponent} at {self.location} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('going', 'Going'),
        ('not going', 'Not going'),
        ('maybe', 'Maybe'),
    )

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('match', 'player')

    def __str__(self):
        return f"{self.player.name} is {self.status} for {self.match}"

class GoalEvent(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField()

    def __str__(self):
        return f"Goal by {self.player.name} at {self.minute}' in {self.match}"

class AssistEvent(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField()

    def __str__(self):
        return f"Assist by {self.player.name} at {self.minute}' in {self.match}"
