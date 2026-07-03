from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Shared utilities, base models and template components."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
