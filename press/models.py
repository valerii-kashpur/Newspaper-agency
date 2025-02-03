from django.db import models
from django.contrib.auth.models import AbstractUser


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    pseudonym = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.pseudonym:
            return f"{self.first_name} {self.last_name} ({self.pseudonym})"
        return f"{self.first_name} {self.last_name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=255, required=True)
    content = models.TextField(required=True)
    published_date = models.DateField(required=True)
    topics = models.ManyToManyField(Topic,
                                    related_name="newspapers")
    publishers = models.ManyToManyField(Redactor, related_name="newspapers")

    def __str__(self):
        return self.title

    def get_topics_display(self):
        return ", ".join(topic.name for topic in self.topics.all())

    def get_publishers_display(self):
        return ", ".join(
            publisher.username for publisher in self.publishers.all())
