from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    name_validator = RegexValidator(
        regex=r'^[A-Za-zА-Яа-яёЁ]+$',
        message="The name should only contain letters."
    )
    min_length_validator = MinLengthValidator(
        3,
        message="The name must be at least 3 characters long."
    )

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    pseudonym = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )

    def __str__(self):
        if self.pseudonym:
            return f"{self.first_name} {self.last_name} ({self.pseudonym})"
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("press:redactor-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    published_date = models.DateField(blank=False, null=False)
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

    class Meta:
        ordering = ['-published_date']
