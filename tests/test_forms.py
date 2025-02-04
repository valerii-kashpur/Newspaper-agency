from django.test import TestCase
from django.contrib.auth import get_user_model
from press.forms import (
    NewspaperForm,
    NewspaperSearchForm,
    RedactorCreationForm,
    RedactorSearchForm,
    TagSearchForm,
)
from press.models import Topic


class NewspaperFormTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Politics")
        self.user = get_user_model().objects.create_user(
            username="editor1", password="testpass123"
        )

    def test_valid_form(self):
        form = NewspaperForm(
            data={
                "title": "Breaking News",
                "content": "Some content...",
                "published_date": "2025-02-04T12:00",
                "topics": [self.topic.id],
                "publishers": [self.user.id],
            }
        )
        self.assertTrue(form.is_valid())

    def test_widgets(self):
        form = NewspaperForm()
        rendered_widget = form.fields["published_date"].widget.render(
            name="published_date", value=None
        )
        self.assertIn('type="datetime-local"', rendered_widget)


class NewspaperSearchFormTest(TestCase):
    def test_valid_form(self):
        form = NewspaperSearchForm(data={"title": "News"})
        self.assertTrue(form.is_valid())

    def test_empty_form_is_valid(self):
        form = NewspaperSearchForm(data={})
        self.assertTrue(form.is_valid())


class RedactorCreationFormTest(TestCase):
    def test_valid_form(self):
        form = RedactorCreationForm(
            data={
                "username": "editor1",
                "password1": "Testpass123!",
                "password2": "Testpass123!",
                "email": "editor@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "pseudonym": "AceWriter",
            }
        )
        self.assertTrue(form.is_valid())


class RedactorSearchFormTest(TestCase):
    def test_valid_form(self):
        form = RedactorSearchForm(
            data={"search_by": "first_name", "search_value": "John"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_choice(self):
        form = RedactorSearchForm(
            data={"search_by": "invalid_field", "search_value": "John"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("search_by", form.errors)

    def test_widgets(self):
        form = RedactorSearchForm()
        self.assertEqual(form.fields["search_by"].widget.attrs["class"], "form-control")
        self.assertEqual(
            form.fields["search_value"].widget.attrs["class"], "form-control"
        )


class TagSearchFormTest(TestCase):
    def test_valid_form(self):
        form = TagSearchForm(data={"name": "Politics"})
        self.assertTrue(form.is_valid())

    def test_empty_form_is_valid(self):
        form = TagSearchForm(data={})
        self.assertTrue(form.is_valid())
