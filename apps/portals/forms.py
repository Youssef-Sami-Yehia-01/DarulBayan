"""Forms used inside the portals' popup modals."""
from django import forms

from .models import Announcement, Grade, Homework


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ["title", "due_date", "attachment", "instructions"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "instructions": forms.Textarea(attrs={"rows": 5}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["title", "score", "max_score", "date", "feedback"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "feedback": forms.Textarea(attrs={"rows": 4}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 5})}
