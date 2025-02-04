from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from press.forms import (NewspaperForm, RedactorCreationForm, TagSearchForm,
                         RedactorSearchForm, NewspaperSearchForm)
from press.mixins import SearchMixin, SearchByMixin
from press.models import Topic, Redactor, Newspaper


def index(request):
    num_newspapers = Newspaper.objects.count()
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()

    context = {
        "num_newspapers": num_newspapers,
        "num_redactors": num_redactors,
        "num_topics": num_topics,
    }

    return render(request, "press/index.html", context=context)


class TopicListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Topic
    template_name = "press/topic_list.html"
    paginate_by = 10

    search_form_class = TagSearchForm
    search_field = "name"


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("press:topic-list")


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("press:topic-list")


class RedactorListView(LoginRequiredMixin, SearchByMixin, SearchMixin,
                       ListView):
    model = Redactor
    template_name = "press/redactor_list.html"
    paginate_by = 10

    search_form_class = RedactorSearchForm
    allowed_search_fields = ["first_name", "last_name", "pseudonym"]


class RedactorDetailView(LoginRequiredMixin, DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related(
        "newspapers__topics"
    )


class RedactorDeleteView(LoginRequiredMixin, DeleteView):
    model = Redactor
    success_url = reverse_lazy("press:redactor-list")


class NewspaperListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Newspaper
    template_name = "press/newspaper_list.html"
    paginate_by = 10

    search_form_class = NewspaperSearchForm
    search_field = "title"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("topics", "publishers")
        return queryset.order_by("-published_date")


class NewspaperDetailView(LoginRequiredMixin, DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("press:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("press:newspaper-list")


class RegisterView(CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


@login_required
def delete_newspaper(request, pk):
    newspaper = get_object_or_404(Newspaper, pk=pk)
    newspaper.delete()
    return HttpResponseRedirect(reverse_lazy("press:newspaper-list"))


@login_required
def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.delete()
    return HttpResponseRedirect(reverse_lazy("press:topic-list"))
