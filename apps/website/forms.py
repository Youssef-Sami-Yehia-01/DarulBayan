from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    """Public contact form on the Enquire page."""

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 6})}
