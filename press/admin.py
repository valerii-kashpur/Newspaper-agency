from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Topic, Redactor, Newspaper


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    model = Redactor
    list_display = (
        "username",
        "first_name",
        "last_name",
        "pseudonym",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "first_name", "last_name", "pseudonym")
    ordering = ("username",)
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("pseudonym",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("pseudonym",)}),)


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "published_date",
        "get_topics_display",
        "get_publishers_display",
    )
    search_fields = ("title", "content")
    list_filter = ("published_date", "topics", "publishers")
