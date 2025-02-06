from django.urls import path

from press.views import (index, TopicListView, RedactorListView,
                         NewspaperListView, delete_newspaper,
                         NewspaperDetailView,
                         NewspaperUpdateView, NewspaperCreateView,
                         RedactorDetailView, RedactorDeleteView,
                         TopicCreateView, delete_topic,
                         TopicUpdateView)

urlpatterns = [
    path("", index, name="index"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspaper/create/", NewspaperCreateView.as_view(),
         name="newspaper-create"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(),
         name="newspaper-detail"),
    path("newspaper/<int:pk>/update/", NewspaperUpdateView.as_view(),
         name="newspaper-update"),
    path("newspaper/<int:pk>/delete/", delete_newspaper,
         name="newspaper-delete"),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
    path("redactor/<int:pk>/", RedactorDetailView.as_view(),
         name="redactor-detail"),
    path("redactor/<int:pk>/delete/", RedactorDeleteView.as_view(),
         name="redactor-delete"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("topic/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topic/<int:pk>/delete/", delete_topic, name="topic-delete"),
    path("topic/<int:pk>/update/", TopicUpdateView.as_view(),
         name="topic-update"),
]

app_name = "press"
