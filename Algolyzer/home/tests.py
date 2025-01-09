from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DashboardViewTest(TestCase):
    def setUp(self):
        # Create a test user with an email for Allauth
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.dashboard_url = reverse("dashboard")

    def test_dashboard_view_redirects_for_anonymous_user(self):
        # Ensure anonymous users are redirected to the login page
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.dashboard_url}"
        )

    def test_dashboard_view_accessible_to_authenticated_user(self):
        # Log in the test user using Allauth-compatible email login
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)  # Should be accessible
        self.assertTemplateUsed(
            response, "home/dashboard.html"
        )  # Ensure the correct template is used

    def test_dashboard_view_displays_username(self):
        # Log in the test user
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.get(self.dashboard_url)
        self.assertContains(
            response, "Logged in as testuser"
        )  # Ensure the email is displayed correctly

    def test_dashboard_view_has_logout_link(self):
        # Log in the test user
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.get(self.dashboard_url)
        self.assertContains(
            response, reverse("account_logout")
        )  # Ensure the logout link is present
