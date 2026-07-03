"""Django admin registration — technical fallback only; the custom
/panel/ app is the primary way to manage site content."""
from django.contrib import admin

from .models import (
    ContentBlock,
    Enquiry,
    Event,
    GalleryCategory,
    GalleryImage,
    InfoPage,
    NewsletterPost,
)

admin.site.register(Event)
admin.site.register(NewsletterPost)
admin.site.register(GalleryCategory)
admin.site.register(GalleryImage)
admin.site.register(Enquiry)
admin.site.register(InfoPage)
admin.site.register(ContentBlock)
