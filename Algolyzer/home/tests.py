from django.test import TestCase
from django.urls import reverse


class HomePageViewTest(TestCase):
    def test_homepage_view_status_code(self):
        """
        Test if the homepage view returns a 200 HTTP status code.
        """
        response = self.client.get(
            reverse("home")
        )  # 'home' is the name of the URL pattern
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_template_used(self):
        """
        Test if the correct template is used by the homepage view.
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_homepage_view_content(self):
        """
        Test if the homepage contains specific content.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Welcome to the Home Page!")
