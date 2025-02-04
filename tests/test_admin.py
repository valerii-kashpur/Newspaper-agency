from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from press.models import Topic, Newspaper


class AdminListDisplayTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="testpass123"
        )
        self.client.login(username="admin", password="testpass123")

        self.topic = Topic.objects.create(name="Politics")
        self.redactor = get_user_model().objects.create_user(
            username="editor1",
            first_name="John",
            last_name="Doe",
            pseudonym="AceWriter",
            password="testpass123",
        )
        self.newspaper = Newspaper.objects.create(
            title="Breaking News",
            content="Some content...",
            published_date="2025-02-04",
        )
        self.newspaper.topics.add(self.topic)
        self.newspaper.publishers.add(self.redactor)

    def test_redactor_list_display(self):
        url = reverse("admin:press_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, "editor1")  # username
        self.assertContains(response, "John")  # first_name
        self.assertContains(response, "Doe")  # last_name
        self.assertContains(response, "AceWriter")  # pseudonym

    def test_newspaper_list_display(self):
        url = reverse("admin:press_newspaper_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Breaking News")  # title
        self.assertContains(response, "Politics")  # get_topics_display
        self.assertContains(response, "editor1")  # get_publishers_display


class AdminSearchAndFilterTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="testpass123"
        )
        self.client.login(username="admin", password="testpass123")

        self.topic = Topic.objects.create(name="Politics")
        self.newspaper = Newspaper.objects.create(
            title="Breaking News",
            content="Some content...",
            published_date="2025-02-04",
        )
        self.newspaper.topics.add(self.topic)

    def test_newspaper_search(self):
        url = reverse("admin:press_newspaper_changelist") + "?q=Breaking"
        response = self.client.get(url)
        self.assertContains(response, "Breaking News")

    def test_newspaper_filter(self):
        url = (
            reverse("admin:press_newspaper_changelist")
            + "?topics__id__exact="
            + str(self.topic.id)
        )
        response = self.client.get(url)
        self.assertContains(response, "Breaking News")
