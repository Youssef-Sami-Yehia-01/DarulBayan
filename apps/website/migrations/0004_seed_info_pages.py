"""Seed the three info pages with the copy from the original site
(darulbayan.co.uk/about, /why-choose-darulbayan, /gcse-a-level).
All of it stays editable from the admin panel."""
from django.db import migrations

PAGES = [
    {
        "title": "About",
        "nav_label": "About",
        "slug": "about",
        "nav_order": 1,
        "intro": (
            "Darulbayan is Aberdeen's Arabic language school, where we foster a love "
            "for the Arabic language and Islamic studies in students of all ages and "
            "backgrounds. We are the first in Aberdeen to provide GCSE and A-Level "
            "Arabic instruction, committed to quality education for both native and "
            "non-native speakers."
        ),
        "blocks": [
            {
                "heading": "Our programs",
                "body": (
                    "Arabic Language — Modern Standard and Classical Arabic.\n"
                    "GCSE and A-Level Arabic — with full exam preparation.\n"
                    "Islamic Studies — focused on religious knowledge.\n"
                    "Classes for ages 5–15, plus specialised adult programs."
                ),
                "order": 1,
            },
            {
                "heading": "Flexible learning options",
                "body": (
                    "We offer one-to-one personalised classes, group-based interactive "
                    "learning, and both face-to-face and online instruction options — "
                    "so every family can find a format that works."
                ),
                "order": 2,
            },
        ],
    },
    {
        "title": "Why Choose Darulbayan?",
        "nav_label": "Why Choose Us?",
        "slug": "why-choose-darulbayan",
        "nav_order": 2,
        "intro": (
            "Families across Aberdeen choose Darulbayan for expert teaching, "
            "engaging lessons and real value."
        ),
        "blocks": [
            {
                "heading": "Expert Native Teachers",
                "body": "Over a decade of teaching experience.",
                "order": 1,
            },
            {
                "heading": "Creative & Interactive Methods",
                "body": "Engaging lessons with group activities.",
                "order": 2,
            },
            {
                "heading": "Sibling Discounts",
                "body": "Affordable learning for families.",
                "order": 3,
            },
            {
                "heading": "First Lesson FREE",
                "body": "Try us out with no commitment!",
                "order": 4,
            },
        ],
    },
    {
        "title": "Expert GCSE and A-Level Tuition",
        "nav_label": "GCSE / A-Level",
        "slug": "gcse-a-level",
        "nav_order": 3,
        "intro": (
            "We prepare students for Edexcel GCSE (9-1) Arabic and Edexcel A-Level "
            "Arabic examinations with a full and supportive learning experience."
        ),
        "blocks": [
            {
                "heading": "Beyond the language",
                "body": (
                    "We go beyond basic language instruction — we teach you to be "
                    "confident and skilled in Arabic, covering translation accuracy "
                    "and essay composition. Our teaching continues throughout the "
                    "week with regular check-ins to reinforce learning and keep up "
                    "momentum."
                ),
                "order": 1,
            },
            {
                "heading": "Our track record",
                "body": (
                    "Over the past four years, our students have predominantly "
                    "achieved high grades — most receiving A grades or above — "
                    "thanks to our focused approach and expert teaching."
                ),
                "order": 2,
            },
            {
                "heading": "A qualification that opens doors",
                "body": (
                    "Arabic qualifications provide professional advantages in "
                    "international relations, business, journalism and translation, "
                    "giving students an edge in the global job market."
                ),
                "order": 3,
            },
        ],
    },
]


def add_pages(apps, schema_editor):
    InfoPage = apps.get_model("website", "InfoPage")
    ContentBlock = apps.get_model("website", "ContentBlock")
    for data in PAGES:
        blocks = data.pop("blocks")
        page, created = InfoPage.objects.get_or_create(slug=data["slug"], defaults=data)
        if created:
            for block in blocks:
                ContentBlock.objects.create(page=page, **block)


def remove_pages(apps, schema_editor):
    InfoPage = apps.get_model("website", "InfoPage")
    InfoPage.objects.filter(slug__in=[p["slug"] for p in PAGES]).delete()


class Migration(migrations.Migration):
    dependencies = [("website", "0003_infopage_contentblock")]
    operations = [migrations.RunPython(add_pages, remove_pages)]
