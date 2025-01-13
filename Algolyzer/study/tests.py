# study/tests.py

from django.test import TestCase
from django.urls import reverse

from .models import Category, Topic


class LandingPageViewTests(TestCase):
    def setUp(self):
        # Create categories and topics for testing
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(
            name="Category 2", parent=self.category1
        )

        self.topic1 = Topic.objects.create(
            title="Topic 1", content="Content for topic 1", category=self.category1
        )
        self.topic2 = Topic.objects.create(
            title="Topic 2", content="Content for topic 2", category=self.category2
        )

    def test_landing_page_status_code(self):
        """Test that the landing page loads correctly"""
        response = self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_categories(self):
        """Test that categories appear on the landing page"""
        response = self.client.get(reverse("landing_page"))
        self.assertContains(response, "Category 1")
        self.assertContains(response, "Category 2")

    def test_filter_topics_by_category(self):
        """Test that topics can be filtered by category"""
        response = self.client.get(
            reverse("landing_page") + "?category=" + str(self.category1.id)
        )
        self.assertContains(response, "Topic 1")
        self.assertNotContains(response, "Topic 2")

    def test_sort_topics_by_title(self):
        """Test that topics can be sorted by title"""
        response = self.client.get(reverse("landing_page") + "?sort=title")
        topics = response.context["topics"]
        self.assertEqual(topics[0].title, "Topic 1")
        self.assertEqual(topics[1].title, "Topic 2")

    def test_sort_topics_by_created_at(self):
        """Test that topics can be sorted by created_at (default)"""
        response = self.client.get(reverse("landing_page") + "?sort=created_at")
        topics = response.context["topics"]
        self.assertEqual(topics[0].title, "Topic 1")
        self.assertEqual(topics[1].title, "Topic 2")


class TopicDetailViewTests(TestCase):
    def setUp(self):
        # Create categories and a topic for testing
        self.category = Category.objects.create(name="Category 1")
        self.topic = Topic.objects.create(
            title="Topic 1",
            content="Detailed content for Topic 1",
            category=self.category,
        )

    def test_topic_detail_view_status_code(self):
        """Test that the topic detail page loads correctly"""
        response = self.client.get(reverse("topic_detail", args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)

    def test_topic_detail_view_content(self):
        """Test that the topic content is correctly displayed"""
        response = self.client.get(reverse("topic_detail", args=[self.topic.id]))
        self.assertContains(response, self.topic.title)
        self.assertContains(response, self.topic.content)

    def test_topic_detail_view_not_found(self):
        """Test that accessing a non-existing topic results in a 404"""
        response = self.client.get(
            reverse("topic_detail", args=[999])
        )  # ID 999 does not exist
        self.assertEqual(response.status_code, 404)


class TopicDetailRedirectTests(TestCase):
    def setUp(self):
        # Create a category and topic
        self.category = Category.objects.create(name="Category 1")
        self.topic = Topic.objects.create(
            title="Topic 1", content="Content for Topic 1", category=self.category
        )

    def test_redirect_to_landing_page(self):
        """Test if trying to view a non-existent topic redirects to a 404"""
        response = self.client.get(
            reverse("topic_detail", args=[999])
        )  # ID 999 does not exist
        self.assertEqual(response.status_code, 404)
