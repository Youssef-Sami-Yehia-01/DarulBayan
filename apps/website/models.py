"""Content managed through the admin panel and shown on the public site."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Event(models.Model):
    """School/community event announced on the Events page."""

    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="events/", blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title


class NewsletterPost(models.Model):
    """News/update article shown on the Newsletter page."""

    title = models.CharField(max_length=200)
    published_date = models.DateField()
    body = models.TextField()
    image = models.ImageField(upload_to="newsletter/", blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("website:newsletter_detail", kwargs={"pk": self.pk})


class GalleryCategory(models.Model):
    """Filter tab on the Gallery page (e.g. Lessons, Events, Trips)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "gallery categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    """Photo in the Gallery, grouped by category."""

    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.PROTECT, related_name="images"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.caption or f"Image #{self.pk}"


class InfoPage(models.Model):
    """Informational site page (About, Why Choose, GCSE/A-Level, ...)
    whose content is fully editable from the admin panel."""

    title = models.CharField(max_length=200)
    nav_label = models.CharField(
        max_length=50, help_text="Short text shown in the navigation bar."
    )
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    intro = models.TextField(blank=True)
    nav_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["nav_order", "id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nav_label or self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("website:info_page", kwargs={"slug": self.slug})


class ContentBlock(models.Model):
    """One section of an InfoPage: optional heading/image plus body text."""

    page = models.ForeignKey(InfoPage, on_delete=models.CASCADE, related_name="blocks")
    heading = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to="pages/", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.heading or f"Block #{self.pk}"


class Enquiry(models.Model):
    """Message submitted through the public Enquire form."""

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    is_handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "enquiries"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d %b %Y}"
