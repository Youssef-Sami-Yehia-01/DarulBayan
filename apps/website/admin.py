"""Django admin registration — technical fallback only; the custom
/panel/ app is the primary way to manage site content."""
from django.contrib import admin

from .models import Enquiry, Event, GalleryCategory, GalleryImage, NewsletterPost

admin.site.register(Event)
admin.site.register(NewsletterPost)
admin.site.register(GalleryCategory)
admin.site.register(GalleryImage)
admin.site.register(Enquiry)
