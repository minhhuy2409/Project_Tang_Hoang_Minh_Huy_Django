from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from team.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile for each User missing one. Sets role=admin if user is superuser, else player.'

    def handle(self, *args, **options):
        users = User.objects.all()
        count_created = 0
        for user in users:
            if not hasattr(user, 'userprofile'):
                role = 'admin' if user.is_superuser else 'player'
                UserProfile.objects.create(user=user, role=role)
                self.stdout.write(self.style.SUCCESS(f'Created UserProfile for user {user.username} as {role}'))
                count_created += 1
        self.stdout.write(self.style.SUCCESS(f'Total user profiles created: {count_created}'))
