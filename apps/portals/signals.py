"""Keeps academic records consistent with user accounts."""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_student_profile(sender, instance, **kwargs):
    """Every user with the student role gets a StudentProfile automatically,
    so panel/teacher views never have to handle a missing profile."""
    if instance.role == instance.Role.STUDENT:
        StudentProfile.objects.get_or_create(user=instance)
