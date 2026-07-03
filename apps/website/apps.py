from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """Public website: pages, events, newsletter, gallery, enquiries."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.website"
    label = "website"
