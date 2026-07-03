from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from apps.core.mixins import NavSectionMixin

from .forms import EnquiryForm
from .models import Event, GalleryCategory, GalleryImage, InfoPage, NewsletterPost


class HomeView(NavSectionMixin, TemplateView):
    """Public homepage: teasers of the latest content in each section."""

    template_name = "website/home.html"
    nav_section = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            events=Event.objects.filter(is_published=True)[:3],
            posts=NewsletterPost.objects.filter(is_published=True)[:3],
            gallery_images=GalleryImage.objects.all()[:8],
        )
        return context


class EventListView(NavSectionMixin, ListView):
    template_name = "website/events.html"
    paginate_by = 9
    nav_section = "events"
    queryset = Event.objects.filter(is_published=True)


class NewsletterListView(NavSectionMixin, ListView):
    template_name = "website/newsletter.html"
    paginate_by = 9
    nav_section = "newsletter"
    queryset = NewsletterPost.objects.filter(is_published=True)


class NewsletterDetailView(NavSectionMixin, DetailView):
    template_name = "website/newsletter_detail.html"
    nav_section = "newsletter"
    queryset = NewsletterPost.objects.filter(is_published=True)


class GalleryView(NavSectionMixin, ListView):
    """Image grid with category filter tabs (?category=<slug>)."""

    template_name = "website/gallery.html"
    paginate_by = 12
    nav_section = "gallery"

    def get_queryset(self):
        queryset = GalleryImage.objects.select_related("category")
        slug = self.request.GET.get("category")
        if slug:
            queryset = queryset.filter(category__slug=slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = GalleryCategory.objects.all()
        context["active_category"] = self.request.GET.get("category", "")
        return context


class InfoPageView(DetailView):
    """Admin-editable content page (About, Why Choose, GCSE/A-Level, ...)."""

    template_name = "website/info_page.html"
    queryset = InfoPage.objects.filter(is_published=True).prefetch_related("blocks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_active"] = self.object.slug
        return context


class EnquireView(NavSectionMixin, SuccessMessageMixin, CreateView):
    """Public contact form; submissions appear in the admin panel."""

    template_name = "website/enquire.html"
    form_class = EnquiryForm
    success_url = reverse_lazy("website:enquire")
    success_message = "Thank you for your enquiry — we will get back to you soon."
    nav_section = "enquire"
