from django.test import TestCase
from django.urls import reverse
from press.models import Newspaper, Redactor, Topic


class IndexViewTests(TestCase):

    def setUp(self):
        topic = Topic.objects.create(name="Test Topic")
        redactor = Redactor.objects.create(
            first_name="John", last_name="Doe", username="johndoe"
        )
        Newspaper.objects.create(
            title="Test Newspaper",
            content="Some content",
            published_date="2025-02-04",
        ).topics.set([topic])
        Newspaper.objects.first().publishers.set([redactor])

    def test_index_view_status_code(self):
        response = self.client.get(reverse("press:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        response = self.client.get(reverse("press:index"))
        self.assertEqual(response.context["num_newspapers"], 1)
        self.assertEqual(response.context["num_redactors"], 1)
        self.assertEqual(response.context["num_topics"], 1)

    def test_index_view_empty_data(self):
        Newspaper.objects.all().delete()
        Redactor.objects.all().delete()
        Topic.objects.all().delete()

        response = self.client.get(reverse("press:index"))
        self.assertEqual(response.context["num_newspapers"], 0)
        self.assertEqual(response.context["num_redactors"], 0)
        self.assertEqual(response.context["num_topics"], 0)
