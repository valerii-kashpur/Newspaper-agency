from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from press.models import Topic, Newspaper


class RedactorModelTest(TestCase):
    def test_str_method_without_pseudonym(self):
        redactor = get_user_model().objects.create_user(
            username="editor1",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )
        self.assertEqual(str(redactor), "John Doe")

    def test_str_method_with_pseudonym(self):
        redactor = get_user_model().objects.create_user(
            username="editor2",
            first_name="Jane",
            last_name="Smith",
            pseudonym="AceWriter",
            password="testpass123",
        )
        self.assertEqual(str(redactor), "Jane Smith (AceWriter)")

    def test_get_absolute_url(self):
        redactor = get_user_model().objects.create_user(
            username="editor3",
            first_name="Alice",
            last_name="Brown",
            password="testpass123",
        )
        self.assertEqual(
            redactor.get_absolute_url(),
            reverse("press:redactor-detail", kwargs={"pk": redactor.pk}),
        )


class NewspaperModelTest(TestCase):
    def setUp(self):
        self.topic1 = Topic.objects.create(name="Politics")
        self.topic2 = Topic.objects.create(name="Sports")

        self.redactor1 = get_user_model().objects.create_user(
            username="editor1",
            first_name="John",
            last_name="Doe",
            password="testpass123",
        )
        self.redactor2 = get_user_model().objects.create_user(
            username="editor2",
            first_name="Jane",
            last_name="Smith",
            password="testpass123",
        )

        self.newspaper = Newspaper.objects.create(
            title="Breaking News",
            content="Some content...",
            published_date="2025-02-04",
        )
        self.newspaper.topics.set([self.topic1, self.topic2])
        self.newspaper.publishers.set([self.redactor1, self.redactor2])

    def test_str_method(self):
        self.assertEqual(str(self.newspaper), "Breaking News")

    def test_get_topics_display(self):
        self.assertEqual(self.newspaper.get_topics_display(), "Politics, Sports")

    def test_get_publishers_display(self):
        self.assertEqual(self.newspaper.get_publishers_display(), "editor1, editor2")


class TopicModelTest(TestCase):
    def test_str_method(self):
        topic = Topic.objects.create(name="Politics")
        self.assertEqual(str(topic), "Politics")
