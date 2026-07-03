from django.apps import AppConfig


class PanelConfig(AppConfig):
    """Custom admin panel: staff-only management of site content and users."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.panel"
    label = "panel"
