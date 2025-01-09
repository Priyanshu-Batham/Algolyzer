from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTest(TestCase):
    def setUp(self):
        """Set up user data for testing"""
        self.email = "testuser@example.com"
        self.username = "testuser"
        self.password = "securepassword123"
        self.user = get_user_model().objects.create_user(
            email=self.email, password=self.password, username=self.username
        )
        EmailAddress.objects.create(
            user=self.user, email=self.email, verified=True, primary=True
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
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)  # Should be accessible
        self.assertTemplateUsed(
            response, "home/dashboard.html"
        )  # Ensure the correct template is used

    def test_dashboard_view_displays_username(self):
        # Log in the test user
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.dashboard_url)
        self.assertContains(
            response, f"Logged in as {self.username}"
        )  # Ensure the email is displayed correctly

    def test_dashboard_view_has_logout_link(self):
        # Log in the test user
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.dashboard_url)
        self.assertContains(
            response, reverse("account_logout")
        )  # Ensure the logout link is present


# Home Page Test
class HomeViewsTest(TestCase):
    def setUp(self):
        """Set up user data for testing"""
        self.email = "testuser@example.com"
        self.username = "testuser"
        self.password = "securepassword123"
        self.user = get_user_model().objects.create_user(
            email=self.email, password=self.password, username=self.username
        )
        EmailAddress.objects.create(
            user=self.user, email=self.email, verified=True, primary=True
        )

        self.home_url = reverse("home")
        self.login_url = reverse("account_login")
        self.logout_url = reverse("account_logout")
        self.dashboard_url = reverse("dashboard")

    def test_home_view_status_code(self):
        """Test if the home view returns a 200 status code"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Test if the home view renders the correct template"""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, "home/home.html")

    def test_home_view_content_for_logged_out_user(self):
        """Test the home view content for a logged-out user"""
        response = self.client.get(self.home_url)
        self.assertContains(response, "This is HOME page view")
        self.assertContains(response, self.login_url)
        self.assertContains(response, self.dashboard_url)

    def test_home_view_content_for_logged_in_user(self):
        """Test the home view content for a logged-in user"""
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.home_url)
        self.assertContains(response, "This is HOME page view")
        self.assertContains(response, self.dashboard_url)
        self.assertNotContains(response, self.login_url)
