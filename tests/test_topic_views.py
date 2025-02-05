from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from press.models import Topic, Newspaper


class TopicViewTestsUnauthenticated(TestCase):
    def test_topic_list_view(self):
        response = self.client.get(reverse("press:topic-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_topic_create_view(self):
        response = self.client.get(reverse("press:topic-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_topic_update_view(self):
        response = self.client.get(reverse("press:topic-update", args=[1]))
        self.assertNotEqual(response.status_code, 200)

    def test_topic_delete_view(self):
        response = self.client.get(reverse("press:topic-delete", args=[1]))
        self.assertNotEqual(response.status_code, 200)


class TopicViewTestsAuthenticated(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")

        self.topic1 = Topic.objects.create(name="Test Topic 1")
        self.topic2 = Topic.objects.create(name="Test Topic 2")

        self.newspaper1 = Newspaper.objects.create(
            title="Political News",
            content="Some content",
            published_date="2024-01-01"
        )
        self.newspaper1.topics.add(self.topic1)

        self.newspaper2 = Newspaper.objects.create(
            title="Sport Weekly",
            content="Some sports content",
            published_date="2024-02-01"
        )
        self.newspaper2.topics.add(self.topic2, self.topic1)

    def test_topic_list_view_status_code(self):
        response = self.client.get(reverse("press:topic-list"))
        self.assertEqual(response.status_code, 200)

    def test_topic_list_view_context(self):
        response = self.client.get(reverse("press:topic-list"))
        self.assertIn("topic_list", response.context)
        self.assertEqual(len(response.context["topic_list"]), 2)

    def test_get_queryset_annotates_newspaper_count(self):
        response = self.client.get(reverse("press:topic-list"))
        self.assertEqual(response.status_code, 200)

        topics = response.context["object_list"]
        topic_counts = {topic.id: topic.newspaper_count for topic in topics}

        expected_counts = {
            self.topic1.id: 2,
            self.topic2.id: 1
        }
        self.assertEqual(topic_counts, expected_counts)

    def test_topic_create_view(self):
        response = self.client.post(
            reverse("press:topic-create"), {"name": "New Topic"}
        )
        self.assertRedirects(response, reverse("press:topic-list"))
        new_topic = get_object_or_404(Topic, name="New Topic")
        self.assertEqual(new_topic.name, "New Topic")

    def test_topic_update_view(self):
        response = self.client.post(
            reverse("press:topic-update", args=[self.topic1.pk]),
            {"name": "Updated Topic"},
        )
        self.assertRedirects(response, reverse("press:topic-list"))
        self.topic1.refresh_from_db()
        self.assertEqual(self.topic1.name, "Updated Topic")

    def test_topic_delete_view(self):
        response = self.client.post(
            reverse("press:topic-delete", args=[self.topic1.pk])
        )
        self.assertRedirects(response, reverse("press:topic-list"))
        with self.assertRaises(Topic.DoesNotExist):
            self.topic1.refresh_from_db()
