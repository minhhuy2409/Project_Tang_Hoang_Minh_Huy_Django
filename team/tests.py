from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from team.models import UserProfile, Player, Match, Attendance


class TeamAppTests(TestCase):

    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpass')
        self.admin_profile = UserProfile.objects.create(user=self.admin_user, role='admin')

        # Create player user
        self.player_user = User.objects.create_user(username='playeruser', password='playerpass')
        self.player_profile = UserProfile.objects.create(user=self.player_user, role='player')
        self.player = Player.objects.create(
            user_profile=self.player_profile,
            name='Test Player',
            shirt_number=10,
            position='FW',
            foot='right',
            playing_style='pressing',
            average_rating=4.5,
            matches_played=5,
            goals=3,
            assists=2,
            health_status='Good'
        )

        # Create a match
        self.match = Match.objects.create(
            opponent='Rivals',
            datetime='2030-01-01 10:00',
            location='Stadium',
            score='2-1',
            tactical_notes='Play aggressively'
        )
        self.match.players.add(self.player)

        self.client = Client()

    def test_admin_dashboard_access(self):
        # Admin user can access dashboard
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get(reverse('team:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')

    def test_player_dashboard_access_forbidden(self):
        # Player user cannot access admin dashboard
        self.client.login(username='playeruser', password='playerpass')
        response = self.client.get(reverse('team:dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_player_profile_view_get_and_post(self):
        self.client.login(username='playeruser', password='playerpass')
        url = reverse('team:player_profile')
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Player Profile')

        # POST with valid data
        data = {
            'name': 'Updated Player',
            'shirt_number': 15,
            'position': 'MF',
            'foot': 'left',
            'playing_style': 'long_pass',
            'average_rating': 4.0,
            'matches_played': 6,
            'goals': 4,
            'assists': 3,
            'health_status': 'Excellent',
        }
        response = self.client.post(url, data)
        self.assertContains(response, 'Profile updated successfully.')
        self.player.refresh_from_db()
        self.assertEqual(self.player.name, 'Updated Player')

    def test_register_attendance_get(self):
        self.client.login(username='playeruser', password='playerpass')
        url = reverse('team:register_attendance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_logout_flow(self):
        login = self.client.login(username='playeruser', password='playerpass')
        self.assertTrue(login)
        # The logout() view requires POST, so do POST here.
        response = self.client.post(reverse('logout'))
        self.assertIn(response.status_code, [302, 301])
