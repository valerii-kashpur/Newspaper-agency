from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from press.models import Newspaper, Topic, Redactor


class NewspaperForm(forms.ModelForm):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    published_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), )

    class Meta:
        model = Newspaper
        fields = "__all__"


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(max_length=155, required=False)


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "pseudonym",
        )


class RedactorSearchForm(forms.Form):
    search_by = forms.ChoiceField(
        choices=[
            ("first_name", "First Name"),
            ("last_name", "Last Name"),
            ("pseudonym", "Pseudonym"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    search_value = forms.CharField(
        max_length=155,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": "Enter search query"})
    )


class TagSearchForm(forms.Form):
    name = forms.CharField(max_length=155, required=False)
