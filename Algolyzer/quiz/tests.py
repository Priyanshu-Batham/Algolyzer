from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from home.models import UserProfile


class QuizHomeViewTests(TestCase):
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
        self.quiz_home_url = reverse(
            "quiz_home"
        )  # Replace with the correct name of your URL

    def test_quiz_home_redirects_if_not_authenticated(self):
        """Test that an unauthenticated user is redirected to the login page"""
        response = self.client.get(self.quiz_home_url)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.quiz_home_url}"
        )

    def test_quiz_home_redirects_to_onboarding_if_no_profile(self):
        """Test that a user without a UserProfile is redirected to the onboarding page"""
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(self.quiz_home_url)
        self.assertRedirects(response, reverse("onboarding"))

    def test_quiz_home_accessible_with_profile(self):
        """Test that a user with a UserProfile can access the quiz home page"""
        self.client.login(email=self.email, password=self.password)
        # Create a UserProfile for the user
        UserProfile.objects.create(user=self.user, dob=timezone.now())

        # Access the quiz home page
        response = self.client.get(self.quiz_home_url)

        # Verify the response status code and template used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/quiz_home.html")
