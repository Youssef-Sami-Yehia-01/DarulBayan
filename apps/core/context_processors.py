"""Context available to every template render."""


def nav_pages(request):
    """Published info pages for the public navigation bar."""
    from apps.website.models import InfoPage  # local import avoids app-loading cycles

    return {"nav_pages": InfoPage.objects.filter(is_published=True)}
