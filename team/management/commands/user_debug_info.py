from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from team.models import UserProfile, Player


class Command(BaseCommand):
    help = "Displays UserProfile and Player info for a given username"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to debug')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'User: {user.username}, is_superuser: {user.is_superuser}, is_active: {user.is_active}')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
            return

        try:
            user_profile = UserProfile.objects.get(user=user)
            self.stdout.write(f'UserProfile exists, role: {user_profile.role}')
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR('UserProfile does not exist'))
            return

        try:
            player = Player.objects.get(user_profile=user_profile)
            self.stdout.write(f'Player exists: {player.name}, shirt number: {player.shirt_number}')
        except Player.DoesNotExist:
            self.stdout.write(self.style.ERROR('Player does not exist'))
