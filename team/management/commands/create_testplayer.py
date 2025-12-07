from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from team.models import UserProfile, Player

class Command(BaseCommand):
    help = 'Create a test player user with player role.'

    def handle(self, *args, **options):
        username = 'testplayer'
        password = 'testpassword123'
        email = 'testplayer@example.com'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists.'))
            return

        user = User.objects.create_user(username=username, email=email, password=password)
        user_profile = UserProfile.objects.create(user=user, role='player')
        Player.objects.create(user_profile=user_profile, name='Test Player', shirt_number=99,
                              position='MF', foot='right', playing_style='pressing')
        self.stdout.write(self.style.SUCCESS(f'Created test player user "{username}" with password "{password}".'))
