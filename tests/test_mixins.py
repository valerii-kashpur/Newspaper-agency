from django.test import TestCase, RequestFactory
from django import forms
from django.views.generic import ListView

from press.models import Newspaper
from press.views import SearchMixin, SearchByMixin


class DummySearchForm(forms.Form):
    search_by = forms.CharField(required=False)
    search_value = forms.CharField(required=False)


class DummySearchView(SearchMixin, SearchByMixin, ListView):
    model = Newspaper
    search_form_class = DummySearchForm
    search_field = "title"
    allowed_search_fields = ["title", "content"]
    template_name = "dummy.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SearchMixinTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.n1 = Newspaper.objects.create(
            title="Breaking News",
            content="Content A",
            published_date="2025-02-04"
        )
        self.n2 = Newspaper.objects.create(
            title="Daily Update",
            content="Content B",
            published_date="2025-02-05"
        )
        self.n3 = Newspaper.objects.create(
            title="Weather Report",
            content="Content C",
            published_date="2025-02-06"
        )

    def _get_view(self, request):
        view = DummySearchView()
        view.request = request
        view.args = ()
        view.kwargs = {}
        view.object_list = view.get_queryset()
        return view

    def test_get_queryset_no_search(self):
        request = self.factory.get("/dummy/")
        view = self._get_view(request)
        qs = view.get_queryset()
        self.assertEqual(qs.count(), 3)

    def test_get_queryset_with_search(self):
        request = self.factory.get("/dummy/", {"search_value": "daily"})
        view = self._get_view(request)
        qs = view.get_queryset()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.n2)

    def test_get_context_data(self):
        request = self.factory.get("/dummy/", {"search_by": "content",
                                               "search_value": "Content B"})
        view = self._get_view(request)
        context = view.get_context_data()
        self.assertIn("search_form", context)
        form = context["search_form"]
        self.assertEqual(form.initial.get("search_by"), "content")
        self.assertEqual(form.initial.get("search_value"), "Content B")

    def test_get_search_field_allowed(self):
        request = self.factory.get("/dummy/", {"search_by": "content"})
        view = self._get_view(request)
        search_field = view.get_search_field()
        self.assertEqual(search_field, "content")

    def test_get_search_field_not_allowed(self):
        request = self.factory.get("/dummy/", {"search_by": "nonexistent"})
        view = self._get_view(request)
        search_field = view.get_search_field()
        self.assertEqual(search_field, "title")
