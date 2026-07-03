from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Single user model for every portal.

    The `role` field decides which portal a user sees after login
    (student / parent / teacher / management). Site administrators are
    regular Django superusers.
    """

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        PARENT = "parent", "Parent"
        TEACHER = "teacher", "Teacher"
        MANAGEMENT = "management", "Management"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.get_full_name() or self.username

    # Convenience checks so templates/views never compare raw strings.
    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_management(self):
        return self.role == self.Role.MANAGEMENT
