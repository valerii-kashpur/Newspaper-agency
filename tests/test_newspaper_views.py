from datetime import datetime

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from press.models import Newspaper, Topic, Redactor
from django.shortcuts import get_object_or_404


class NewspaperViewTestsUnauthenticated(TestCase):
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

    def test_newspaper_list_view(self):
        response = self.client.get(reverse("press:newspaper-list"))
        self.assertRedirects(response, "/accounts/login/?next=/newspaper/")
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_detail_view(self):
        response = self.client.get(
            reverse("press:newspaper-detail", args=[self.newspaper.id]))
        self.assertRedirects(response,
                             "/accounts/login/?next=/newspaper/{}/".format(
                                 self.newspaper.id))
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_create_view(self):
        response = self.client.get(reverse("press:newspaper-create"))
        self.assertRedirects(response,
                             "/accounts/login/?next=/newspaper/create/")
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_update_view(self):
        response = self.client.get(
            reverse("press:newspaper-update", args=[self.newspaper.id]))
        self.assertRedirects(response,
                             "/accounts/login/?next=/newspaper/{}/update/".format(
                                 self.newspaper.id))
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_delete_view(self):
        response = self.client.post(
            reverse("press:newspaper-delete", args=[self.newspaper.id]))
        self.assertRedirects(response,
                             "/accounts/login/?next=/newspaper/{}/delete/".format(
                                 self.newspaper.id))
        self.assertNotEqual(response.status_code, 200)


class NewspaperViewTestsAuthenticated(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",
                                                         password="password123")
        self.client.login(username="testuser", password="password123")
        self.topic = Topic.objects.create(name="Politics")
        self.redactor = Redactor.objects.create(username="redactor1")
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Content of the newspaper",
            published_date="2025-02-04",
        )
        self.newspaper.topics.add(self.topic)
        self.newspaper.publishers.add(self.redactor)

    def test_newspaper_list_view(self):
        response = self.client.get(reverse("press:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Newspaper")
        self.assertTemplateUsed(response, "press/newspaper_list.html")

    def test_newspaper_detail_view(self):
        response = self.client.get(reverse("press:newspaper-detail",
                                           kwargs={"pk": self.newspaper.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Newspaper")
        self.assertContains(response, "Politics")
        self.assertTemplateUsed(response, "press/newspaper_detail.html")

    def test_newspaper_create_view(self):
        response = self.client.get(reverse("press:newspaper-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "press/newspaper_form.html")

    def test_newspaper_create_view_post(self):
        data = {
            "title": "New Newspaper",
            "content": "Content of new newspaper",
            "published_date": "2025-02-04T12:00",
            "topics": [self.topic.pk],
            "publishers": [self.redactor.pk],
        }
        response = self.client.post(reverse("press:newspaper-create"), data)
        self.assertRedirects(response, reverse("press:newspaper-list"))
        self.assertEqual(Newspaper.objects.count(), 2)

    def test_newspaper_update_view(self):
        response = self.client.get(reverse("press:newspaper-update",
                                           kwargs={"pk": self.newspaper.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "press/newspaper_form.html")

    def test_newspaper_update_view_post(self):
        data = {
            "title": "Updated Newspaper",
            "content": "Updated content of the newspaper",
            "published_date": "2025-02-04T12:00",
            "topics": [self.topic.pk],
            "publishers": [self.redactor.pk],
        }
        response = self.client.post(reverse("press:newspaper-update",
                                            kwargs={"pk": self.newspaper.pk}),
                                    data)
        self.assertRedirects(response, reverse("press:newspaper-list"))
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Updated Newspaper")

    def test_newspaper_delete_view(self):
        response = self.client.post(reverse("press:newspaper-delete",
                                            kwargs={"pk": self.newspaper.pk}))
        self.assertRedirects(response, reverse("press:newspaper-list"))
        self.assertEqual(Newspaper.objects.count(), 0)
