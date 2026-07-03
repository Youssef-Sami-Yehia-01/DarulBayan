"""Forms rendered inside the admin panel's popup modals."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from apps.website.models import Event, GalleryCategory, GalleryImage, NewsletterPost

User = get_user_model()


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "time", "location", "image", "description", "is_published"]
        # type="date"/"time" inputs only accept ISO-formatted values,
        # so the format must be forced (Django would localize it otherwise).
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "time": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class NewsletterPostForm(forms.ModelForm):
    class Meta:
        model = NewsletterPost
        fields = ["title", "published_date", "image", "body", "is_published"]
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "body": forms.Textarea(attrs={"rows": 8}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["image", "caption", "category"]


class GalleryCategoryForm(forms.ModelForm):
    class Meta:
        model = GalleryCategory
        fields = ["name"]


class UserCreateForm(UserCreationForm):
    """Create any account (student/parent/teacher/management) from the panel.
    `is_staff` grants access to this admin panel."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "phone", "is_staff"]


class UserUpdateForm(forms.ModelForm):
    """Edit an account; passwords are managed separately."""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "phone", "is_staff", "is_active"]
