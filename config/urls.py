"""Root URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("panel/", include("apps.panel.urls")),
    path("portal/", include("apps.portals.urls")),
    path("", include("apps.accounts.urls")),
    path("", include("apps.website.urls")),  # keep last: ends in a slug catch-all
]

# Serve local media uploads in development when R2 is not configured.
if settings.DEBUG and not settings.USE_R2:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
