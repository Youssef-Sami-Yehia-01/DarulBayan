from django.apps import AppConfig


class PortalsConfig(AppConfig):
    """Student, parent and teacher portals + academic records."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.portals"
    label = "portals"

    def ready(self):
        from . import signals  # noqa: F401  (connects post_save handlers)
