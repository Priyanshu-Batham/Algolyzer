from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from home.models import UserProfile

from .models import Question, QuizProgress, Topic, UserAnswer


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
        self.assertTemplateUsed(response, "quiz/home.html")


class QuizModelsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
            username="testuser",
        )
        self.topic = Topic.objects.create(name="Math")
        self.question = Question.objects.create(
            topic=self.topic,
            text="What is 2+2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_answer="b",
        )
        self.progress = QuizProgress.objects.create(
            user=self.user, topic=self.topic, current_question=0
        )

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, "Math")

    def test_question_creation(self):
        self.assertEqual(self.question.text, "What is 2+2?")
        self.assertEqual(self.question.correct_answer, "b")

    def test_user_answer_creation(self):
        answer = UserAnswer.objects.create(
            topic=self.topic,
            user=self.user,
            question=self.question,
            selected_answer="b",
        )
        self.assertEqual(answer.is_correct, True)

    def test_quiz_progress_creation(self):
        self.assertEqual(self.progress.user, self.user)
        self.assertEqual(self.progress.topic, self.topic)
        self.assertEqual(self.progress.current_question, 0)


class QuizViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
            username="testuser",
        )
        self.topic = Topic.objects.create(name="Math")
        self.question = Question.objects.create(
            topic=self.topic,
            text="What is 2+2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_answer="b",
        )
        self.progress = QuizProgress.objects.create(
            user=self.user, topic=self.topic, current_question=0
        )
        self.client.login(email="testuser@example.com", password="securepassword123")
        UserProfile.objects.create(user=self.user, dob=timezone.now())

    def test_quiz_home(self):
        response = self.client.get(reverse("quiz_home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Math")

    def test_quiz_topic(self):
        response = self.client.get(reverse("quiz_topic", args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)

    def test_quiz_start(self):
        response = self.client.get(reverse("quiz_start", args=[self.topic.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to quiz question

    def test_quiz_question(self):
        response = self.client.get(reverse("quiz_question", args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)

    def test_quiz_results(self):
        UserAnswer.objects.create(
            topic=self.topic,
            user=self.user,
            question=self.question,
            selected_answer="b",
        )
        self.progress.current_question = 1
        self.progress.completed = True
        self.progress.save()
        response = self.client.get(reverse("quiz_results", args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)


class QuizURLsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
            username="testuser",
        )
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.topic = Topic.objects.create(name="Math")
        self.question = Question.objects.create(
            topic=self.topic,
            text="What is 2+2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_answer="b",
        )
        self.client.login(email="testuser@example.com", password="securepassword123")
        UserProfile.objects.create(user=self.user, dob=timezone.now())

    def test_url_quiz_home(self):
        url = reverse("quiz_home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_quiz_topic(self):
        url = reverse("quiz_topic", args=[self.topic.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_quiz_start(self):
        url = reverse("quiz_start", args=[self.topic.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to quiz question

    def test_url_quiz_question(self):
        pre_url = reverse("quiz_start", args=[self.topic.id])
        url = reverse("quiz_question", args=[self.topic.id])
        self.client.get(pre_url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_quiz_results(self):
        UserAnswer.objects.create(
            topic=self.topic,
            user=self.user,
            question=self.question,
            selected_answer="b",
        )
        QuizProgress.objects.create(
            user=self.user, topic=self.topic, current_question=1, completed=True
        )
        url = reverse("quiz_results", args=[self.topic.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
