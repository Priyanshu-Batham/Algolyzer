import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import UserProfile


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

    def test_dashboard_view_displays_level_xp(self):
        self.client.login(email=self.email, password=self.password)
        user_profile = UserProfile.objects.create(user=self.user, dob=timezone.now())

        response = self.client.get(self.dashboard_url)
        self.assertContains(response, f"Level: {user_profile.level}")
        self.assertContains(response, f"XP: {user_profile.xp}")
        self.assertNotContains(response, reverse("onboarding"))

    def test_dashboard_view_not_displays_level_xp_on_incomplete_profile(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.dashboard_url)
        self.assertNotContains(response, "Level:")
        self.assertNotContains(response, "XP:")
        self.assertContains(response, reverse("onboarding"))


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


class OnboardingViewTests(TestCase):
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

        self.url = reverse("onboarding")  # URL for onboarding view
        self.login_url = reverse("account_login")
        self.logout_url = reverse("account_logout")
        self.dashboard_url = reverse("dashboard")

    def test_redirect_to_dashboard_if_user_profile_exists(self):
        # Create a UserProfile for the user
        UserProfile.objects.create(user=self.user, dob=timezone.now())

        # Login with the test user
        self.client.login(email=self.email, password=self.password)

        # Send a GET request to the onboarding page
        response = self.client.get(self.url)

        # Check if the response is a redirect to the dashboard
        self.assertRedirects(response, reverse("dashboard"))

    def test_onboarding_form_is_displayed_if_user_profile_does_not_exist(self):
        # Ensure the user doesn't have a profile
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())

        # Login with the test user
        self.client.login(email=self.email, password=self.password)

        # Send a GET request to the onboarding page
        response = self.client.get(self.url)

        # Check if the response contains the onboarding form
        self.assertContains(response, '<form method="post"')

    def test_create_user_profile_on_valid_post(self):
        # Login with the test user
        self.client.login(email=self.email, password=self.password)

        # Send a POST request to create a profile with valid data
        data = {"dob": "2000-01-01"}  # Example date of birth
        response = self.client.post(self.url, data)

        # Check if the UserProfile was created
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

        # Check if the response redirects to the dashboard
        self.assertRedirects(response, reverse("dashboard"))

        # Check if the UserProfile data was saved correctly
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.dob, datetime.date(2000, 1, 1))

    def test_no_profile_creation_on_invalid_post(self):
        # Login with the test user
        self.client.login(email=self.email, password=self.password)

        # Send a POST request with invalid data (e.g., empty dob)
        data = {"dob": ""}  # Invalid date of birth (empty string)
        self.client.post(self.url, data)

        # Check if the UserProfile is not created
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())
