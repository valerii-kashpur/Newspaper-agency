from django.test import TestCase, RequestFactory
from django.views.generic import ListView
from django.db import models
from django import forms
from django.db.models import Count

from press.mixins import SearchMixin
from press.models import Topic


class TopicSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)


class TopicListView(SearchMixin, ListView):
    model = Topic
    search_form_class = TopicSearchForm
    search_field = "name"

    def get_queryset(self):
        return super().get_queryset().annotate(
            newspaper_count=Count("newspapers"))


class SearchMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        Topic.objects.create(name="Politics")
        Topic.objects.create(name="Sports")
        Topic.objects.create(name="Technology")

    def test_search_by_name(self):
        request = self.factory.get("/", {"name": "Sports"})
        view = TopicListView()
        view.request = request
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().name, "Sports")

    def test_search_no_results(self):
        request = self.factory.get("/", {"name": "Health"})
        view = TopicListView()
        view.request = request
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 0)

    def test_context_data(self):
        request = self.factory.get("/", {"name": "Politics"})

        view = TopicListView()
        view.request = request
        view.object_list = view.get_queryset()

        context = view.get_context_data()

        self.assertEqual(context["search_form"].initial["name"], "Politics")
