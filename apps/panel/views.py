"""Admin panel views.

Modal protocol (see static/js/modal.js):
  GET  -> HTML fragment (form or confirmation) rendered inside the modal
  POST -> 204 on success (modal.js then reloads the page)
          400 + re-rendered fragment when validation fails
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from apps.core.mixins import NavSectionMixin
from apps.website.models import (
    Enquiry,
    Event,
    GalleryCategory,
    GalleryImage,
    NewsletterPost,
)

from . import forms

User = get_user_model()


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only staff accounts may use the admin panel."""

    def test_func(self):
        return self.request.user.is_staff


# --- Generic building blocks -------------------------------------------------


class PanelListView(StaffRequiredMixin, NavSectionMixin, ListView):
    """Paginated table used by every resource list. Subclasses set the
    model, visible columns and the URL names of their modal views."""

    template_name = "panel/crud/list.html"
    paginate_by = 20
    title = ""
    columns = ()      # (field, label) pairs rendered by the generic table
    create_url = ""   # URL name for the "Add" modal ("" hides the button)
    edit_url = ""     # URL name for the row "Edit" modal
    delete_url = ""   # URL name for the row "Delete" modal


class ModalFormMixin(StaffRequiredMixin):
    """Create/Update views opened inside the popup modal."""

    template_name = "panel/crud/form_modal.html"
    title = ""

    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=400)


class ModalDeleteView(StaffRequiredMixin, DeleteView):
    """Delete confirmation opened inside the popup modal."""

    template_name = "panel/crud/confirm_delete.html"

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                error="This item is still used by other content and cannot be deleted."
            )
            return self.render_to_response(context, status=400)
        return HttpResponse(status=204)


# --- Dashboard & auth ---------------------------------------------------------


class DashboardView(StaffRequiredMixin, NavSectionMixin, TemplateView):
    template_name = "panel/dashboard.html"
    nav_section = "dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            event_count=Event.objects.count(),
            post_count=NewsletterPost.objects.count(),
            image_count=GalleryImage.objects.count(),
            user_count=User.objects.count(),
            open_enquiries=Enquiry.objects.filter(is_handled=False)[:5],
            open_enquiry_count=Enquiry.objects.filter(is_handled=False).count(),
        )
        return context


# --- Events -------------------------------------------------------------------


class EventListView(PanelListView):
    model = Event
    nav_section = "events"
    title = "Events"
    columns = (("title", "Title"), ("date", "Date"), ("location", "Location"), ("is_published", "Published"))
    create_url, edit_url, delete_url = "panel:event_add", "panel:event_edit", "panel:event_delete"


class EventCreateView(ModalFormMixin, CreateView):
    model = Event
    form_class = forms.EventForm
    title = "Add event"


class EventUpdateView(ModalFormMixin, UpdateView):
    model = Event
    form_class = forms.EventForm
    title = "Edit event"


class EventDeleteView(ModalDeleteView):
    model = Event


# --- Newsletter ----------------------------------------------------------------


class NewsletterListView(PanelListView):
    model = NewsletterPost
    nav_section = "newsletter"
    title = "Newsletter"
    columns = (("title", "Title"), ("published_date", "Published on"), ("is_published", "Published"))
    create_url, edit_url, delete_url = "panel:post_add", "panel:post_edit", "panel:post_delete"


class NewsletterCreateView(ModalFormMixin, CreateView):
    model = NewsletterPost
    form_class = forms.NewsletterPostForm
    title = "Add newsletter post"


class NewsletterUpdateView(ModalFormMixin, UpdateView):
    model = NewsletterPost
    form_class = forms.NewsletterPostForm
    title = "Edit newsletter post"


class NewsletterDeleteView(ModalDeleteView):
    model = NewsletterPost


# --- Gallery --------------------------------------------------------------------


class GalleryListView(StaffRequiredMixin, NavSectionMixin, ListView):
    """Thumbnail grid instead of the generic table."""

    model = GalleryImage
    template_name = "panel/gallery_list.html"
    paginate_by = 24
    nav_section = "gallery"
    title = "Gallery"

    def get_queryset(self):
        return GalleryImage.objects.select_related("category")


class GalleryImageCreateView(ModalFormMixin, CreateView):
    model = GalleryImage
    form_class = forms.GalleryImageForm
    title = "Add image"


class GalleryImageUpdateView(ModalFormMixin, UpdateView):
    model = GalleryImage
    form_class = forms.GalleryImageForm
    title = "Edit image"


class GalleryImageDeleteView(ModalDeleteView):
    model = GalleryImage


class GalleryCategoryListView(PanelListView):
    model = GalleryCategory
    nav_section = "gallery"
    title = "Gallery categories"
    columns = (("name", "Name"),)
    create_url, edit_url, delete_url = "panel:category_add", "panel:category_edit", "panel:category_delete"


class GalleryCategoryCreateView(ModalFormMixin, CreateView):
    model = GalleryCategory
    form_class = forms.GalleryCategoryForm
    title = "Add category"


class GalleryCategoryUpdateView(ModalFormMixin, UpdateView):
    model = GalleryCategory
    form_class = forms.GalleryCategoryForm
    title = "Edit category"


class GalleryCategoryDeleteView(ModalDeleteView):
    model = GalleryCategory


# --- Enquiries -------------------------------------------------------------------


class EnquiryListView(PanelListView):
    model = Enquiry
    template_name = "panel/enquiries.html"
    nav_section = "enquiries"
    title = "Enquiries"
    columns = (("name", "Name"), ("email", "Email"), ("created_at", "Received"), ("is_handled", "Handled"))
    delete_url = "panel:enquiry_delete"


class EnquiryDetailView(StaffRequiredMixin, DetailView):
    """Read-only message fragment shown inside the modal."""

    model = Enquiry
    template_name = "panel/enquiry_detail_modal.html"


class EnquiryToggleHandledView(StaffRequiredMixin, View):
    """Row action: flip the handled flag and return to the list."""

    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.is_handled = not enquiry.is_handled
        enquiry.save(update_fields=["is_handled"])
        return redirect("panel:enquiries")


class EnquiryDeleteView(ModalDeleteView):
    model = Enquiry


# --- Users -------------------------------------------------------------------------


class UserListView(PanelListView):
    model = User
    nav_section = "users"
    title = "Users"
    columns = (
        ("username", "Username"),
        ("first_name", "First name"),
        ("last_name", "Last name"),
        ("email", "Email"),
        ("role", "Role"),
        ("is_staff", "Panel access"),
        ("is_active", "Active"),
    )
    create_url, edit_url, delete_url = "panel:user_add", "panel:user_edit", "panel:user_delete"

    def get_queryset(self):
        return User.objects.order_by("username")


class UserCreateView(ModalFormMixin, CreateView):
    model = User
    form_class = forms.UserCreateForm
    title = "Add user"


class UserUpdateView(ModalFormMixin, UpdateView):
    model = User
    form_class = forms.UserUpdateForm
    title = "Edit user"


class UserDeleteView(ModalDeleteView):
    model = User
