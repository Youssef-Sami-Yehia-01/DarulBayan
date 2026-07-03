"""Idempotent superuser bootstrap, safe to run on every deploy.

Reads DJANGO_SUPERUSER_USERNAME / _EMAIL / _PASSWORD from the environment
(Render has no free shell access, so `createsuperuser` can't be run there).
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the superuser defined by DJANGO_SUPERUSER_* env vars."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        if not (username and password):
            self.stdout.write("DJANGO_SUPERUSER_* not set; skipping.")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username, defaults={"email": email}
        )
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.role = User.Role.MANAGEMENT
        user.set_password(password)
        user.save()
        self.stdout.write(f"Superuser '{username}' {'created' if created else 'updated'}.")
