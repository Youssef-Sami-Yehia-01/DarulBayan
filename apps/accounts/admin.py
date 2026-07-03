from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class RoleUserAdmin(UserAdmin):
    """Django admin registration; kept as a technical fallback while the
    custom admin panel is the primary way to manage users."""

    list_display = ("username", "get_full_name", "email", "role", "is_active")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (("Portal", {"fields": ("role", "phone")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Portal", {"fields": ("role", "phone")}),)
