from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Authentication and the role-based User model for all portals."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
