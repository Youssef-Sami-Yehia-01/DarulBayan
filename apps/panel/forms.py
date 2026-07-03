"""Forms rendered inside the admin panel's popup modals."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from apps.portals.models import Announcement, ClassGroup, StudentProfile
from apps.website.models import (
    ContentBlock,
    Event,
    GalleryCategory,
    GalleryImage,
    InfoPage,
    NewsletterPost,
)

User = get_user_model()

# type="date"/"time" inputs only accept ISO-formatted values, so the
# format must be forced (Django would localize the initial value otherwise).
DATE_INPUT = forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
TIME_INPUT = forms.TimeInput(attrs={"type": "time"}, format="%H:%M")


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "time", "location", "image", "description", "is_published"]
        widgets = {
            "date": DATE_INPUT,
            "time": TIME_INPUT,
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class NewsletterPostForm(forms.ModelForm):
    class Meta:
        model = NewsletterPost
        fields = ["title", "published_date", "image", "body", "is_published"]
        widgets = {
            "published_date": DATE_INPUT,
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


class InfoPageForm(forms.ModelForm):
    """Slug stays auto-generated so page URLs don't silently change."""

    class Meta:
        model = InfoPage
        fields = ["title", "nav_label", "intro", "nav_order", "is_published"]
        widgets = {"intro": forms.Textarea(attrs={"rows": 4})}


class ContentBlockForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = ["heading", "body", "image", "order"]
        widgets = {"body": forms.Textarea(attrs={"rows": 6})}


class ClassGroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        fields = ["name", "teacher", "schedule"]


class StudentProfileForm(forms.ModelForm):
    """Profiles are created automatically with the user; the panel edits
    class placement and parent links."""

    class Meta:
        model = StudentProfile
        fields = ["class_group", "parents", "date_of_birth", "notes"]
        widgets = {
            "date_of_birth": DATE_INPUT,
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "class_group", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 5})}


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
