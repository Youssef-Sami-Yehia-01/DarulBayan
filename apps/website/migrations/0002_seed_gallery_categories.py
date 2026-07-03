"""Seed the gallery filter categories used on the original site."""
from django.db import migrations
from django.utils.text import slugify

CATEGORIES = ["Lessons", "Events", "GCSE / A-Level", "Trips"]


def add_categories(apps, schema_editor):
    GalleryCategory = apps.get_model("website", "GalleryCategory")
    for name in CATEGORIES:
        GalleryCategory.objects.get_or_create(name=name, defaults={"slug": slugify(name)})


def remove_categories(apps, schema_editor):
    GalleryCategory = apps.get_model("website", "GalleryCategory")
    GalleryCategory.objects.filter(name__in=CATEGORIES).delete()


class Migration(migrations.Migration):
    dependencies = [("website", "0001_initial")]
    operations = [migrations.RunPython(add_categories, remove_categories)]
