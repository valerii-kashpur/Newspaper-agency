from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from press.models import Topic, Redactor, Newspaper


class RedactorViewTestsUnauthenticated(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Politics")
        self.redactor = Redactor.objects.create(username="redactor1")
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Content of the newspaper",
            published_date="2025-02-04",
        )
        self.newspaper.topics.add(self.topic)
        self.newspaper.publishers.add(self.redactor)

    def test_redactor_list_view(self):
        response = self.client.get(reverse("press:redactor-list"))
        self.assertRedirects(response, "/accounts/login/?next=/redactor/")
        self.assertNotEqual(response.status_code, 200)

    def test_redactor_detail_view(self):
        response = self.client.get(
            reverse("press:redactor-detail", args=[self.redactor.id]))
        self.assertRedirects(response,
                             "/accounts/login/?next=/redactor/{}/".format(
                                 self.redactor.id))
        self.assertNotEqual(response.status_code, 200)

    def test_redactor_delete_view(self):
        response = self.client.post(
            reverse("press:redactor-delete", args=[self.redactor.id]))
        self.assertRedirects(response,
                             "/accounts/login/?next=/redactor/{}/delete/".format(
                                 self.redactor.id))
        self.assertNotEqual(response.status_code, 200)


class RedactorViewTestsAuthenticated(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",
                                                         password="password")
        self.client.login(username="testuser", password="password")
        self.topic = Topic.objects.create(name="Politics")
        self.redactor = self.user
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Content of the newspaper",
            published_date="2025-02-04",
        )
        self.newspaper.topics.add(self.topic)
        self.newspaper.publishers.add(self.redactor)

    def test_redactor_list_view(self):
        response = self.client.get(reverse("press:redactor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_redactor_detail_view(self):
        response = self.client.get(
            reverse("press:redactor-detail", args=[self.redactor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_redactor_delete_view(self):
        redactor = get_user_model().objects.create_user(username="del_me",
                                                        password="password")
        response = self.client.post(
            reverse("press:redactor-delete", args=[redactor.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.get("PATH_INFO"),
                         reverse("press:redactor-list"))
        self.assertEqual(get_user_model().objects.count(), 1)
