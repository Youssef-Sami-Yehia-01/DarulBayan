"""Admin panel views (staff only). Modal CRUD building blocks live in
apps.core.views; this module wires them to each managed resource."""
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from apps.core.mixins import NavSectionMixin
from apps.core.views import BaseModalDeleteView, ModalFormMixin
from apps.portals.models import Announcement, ClassGroup, StudentProfile
from apps.website.models import (
    ContentBlock,
    Enquiry,
    Event,
    GalleryCategory,
    GalleryImage,
    InfoPage,
    NewsletterPost,
)

from . import forms

User = get_user_model()


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only staff accounts may use the admin panel."""

    def test_func(self):
        return self.request.user.is_staff


class PanelListView(StaffRequiredMixin, NavSectionMixin, ListView):
    """Paginated table used by every resource list. Subclasses set the
    model, visible columns and the URL names of their modal views."""

    template_name = "panel/crud/list.html"
    paginate_by = 20
    title = ""
    columns = ()      # (field, label) pairs rendered by the generic table
    create_url = ""   # URL name for the "Add" modal ("" hides the button)
    edit_url = ""     # URL name for the row "Edit" modal ("" hides it)
    delete_url = ""   # URL name for the row "Delete" modal ("" hides it)


class PanelModalFormMixin(StaffRequiredMixin, ModalFormMixin):
    """Create/Update modal restricted to staff."""


class PanelModalDeleteView(StaffRequiredMixin, BaseModalDeleteView):
    """Delete-confirmation modal restricted to staff."""


# --- Dashboard -----------------------------------------------------------


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
            class_count=ClassGroup.objects.count(),
            open_enquiries=Enquiry.objects.filter(is_handled=False)[:5],
            open_enquiry_count=Enquiry.objects.filter(is_handled=False).count(),
        )
        return context


# --- Info pages & their content blocks -----------------------------------


class InfoPageListView(PanelListView):
    model = InfoPage
    template_name = "panel/pages.html"
    nav_section = "pages"
    title = "Pages"
    columns = (("title", "Title"), ("nav_label", "Nav label"), ("nav_order", "Order"), ("is_published", "Published"))
    create_url, edit_url, delete_url = "panel:page_add", "panel:page_edit", "panel:page_delete"


class InfoPageCreateView(PanelModalFormMixin, CreateView):
    model = InfoPage
    form_class = forms.InfoPageForm
    title = "Add page"


class InfoPageUpdateView(PanelModalFormMixin, UpdateView):
    model = InfoPage
    form_class = forms.InfoPageForm
    title = "Edit page"


class InfoPageDeleteView(PanelModalDeleteView):
    model = InfoPage


class ContentBlockListView(StaffRequiredMixin, NavSectionMixin, DetailView):
    """Blocks of one page, in order, with modal CRUD."""

    model = InfoPage
    template_name = "panel/page_blocks.html"
    nav_section = "pages"
    context_object_name = "page"


class ContentBlockCreateView(PanelModalFormMixin, CreateView):
    model = ContentBlock
    form_class = forms.ContentBlockForm
    title = "Add section"

    def form_valid(self, form):
        form.instance.page = get_object_or_404(InfoPage, pk=self.kwargs["page_pk"])
        return super().form_valid(form)


class ContentBlockUpdateView(PanelModalFormMixin, UpdateView):
    model = ContentBlock
    form_class = forms.ContentBlockForm
    title = "Edit section"


class ContentBlockDeleteView(PanelModalDeleteView):
    model = ContentBlock


# --- Events ----------------------------------------------------------------


class EventListView(PanelListView):
    model = Event
    nav_section = "events"
    title = "Events"
    columns = (("title", "Title"), ("date", "Date"), ("location", "Location"), ("is_published", "Published"))
    create_url, edit_url, delete_url = "panel:event_add", "panel:event_edit", "panel:event_delete"


class EventCreateView(PanelModalFormMixin, CreateView):
    model = Event
    form_class = forms.EventForm
    title = "Add event"


class EventUpdateView(PanelModalFormMixin, UpdateView):
    model = Event
    form_class = forms.EventForm
    title = "Edit event"


class EventDeleteView(PanelModalDeleteView):
    model = Event


# --- Newsletter --------------------------------------------------------------


class NewsletterListView(PanelListView):
    model = NewsletterPost
    nav_section = "newsletter"
    title = "Newsletter"
    columns = (("title", "Title"), ("published_date", "Published on"), ("is_published", "Published"))
    create_url, edit_url, delete_url = "panel:post_add", "panel:post_edit", "panel:post_delete"


class NewsletterCreateView(PanelModalFormMixin, CreateView):
    model = NewsletterPost
    form_class = forms.NewsletterPostForm
    title = "Add newsletter post"


class NewsletterUpdateView(PanelModalFormMixin, UpdateView):
    model = NewsletterPost
    form_class = forms.NewsletterPostForm
    title = "Edit newsletter post"


class NewsletterDeleteView(PanelModalDeleteView):
    model = NewsletterPost


# --- Gallery ------------------------------------------------------------------


class GalleryListView(StaffRequiredMixin, NavSectionMixin, ListView):
    """Thumbnail grid instead of the generic table."""

    model = GalleryImage
    template_name = "panel/gallery_list.html"
    paginate_by = 24
    nav_section = "gallery"
    title = "Gallery"

    def get_queryset(self):
        return GalleryImage.objects.select_related("category")


class GalleryImageCreateView(PanelModalFormMixin, CreateView):
    model = GalleryImage
    form_class = forms.GalleryImageForm
    title = "Add image"


class GalleryImageUpdateView(PanelModalFormMixin, UpdateView):
    model = GalleryImage
    form_class = forms.GalleryImageForm
    title = "Edit image"


class GalleryImageDeleteView(PanelModalDeleteView):
    model = GalleryImage


class GalleryCategoryListView(PanelListView):
    model = GalleryCategory
    nav_section = "gallery"
    title = "Gallery categories"
    columns = (("name", "Name"),)
    create_url, edit_url, delete_url = "panel:category_add", "panel:category_edit", "panel:category_delete"


class GalleryCategoryCreateView(PanelModalFormMixin, CreateView):
    model = GalleryCategory
    form_class = forms.GalleryCategoryForm
    title = "Add category"


class GalleryCategoryUpdateView(PanelModalFormMixin, UpdateView):
    model = GalleryCategory
    form_class = forms.GalleryCategoryForm
    title = "Edit category"


class GalleryCategoryDeleteView(PanelModalDeleteView):
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


class EnquiryDeleteView(PanelModalDeleteView):
    model = Enquiry


# --- Announcements ------------------------------------------------------------------


class AnnouncementListView(PanelListView):
    model = Announcement
    nav_section = "announcements"
    title = "Announcements"
    columns = (("title", "Title"), ("class_group", "Class"), ("created_at", "Posted"))
    create_url, edit_url, delete_url = "panel:announcement_add", "panel:announcement_edit", "panel:announcement_delete"


class AnnouncementCreateView(PanelModalFormMixin, CreateView):
    model = Announcement
    form_class = forms.AnnouncementForm
    title = "Add announcement"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(PanelModalFormMixin, UpdateView):
    model = Announcement
    form_class = forms.AnnouncementForm
    title = "Edit announcement"


class AnnouncementDeleteView(PanelModalDeleteView):
    model = Announcement


# --- Classes ----------------------------------------------------------------------


class ClassGroupListView(PanelListView):
    model = ClassGroup
    nav_section = "classes"
    title = "Classes"
    columns = (("name", "Name"), ("teacher", "Teacher"), ("schedule", "Schedule"))
    create_url, edit_url, delete_url = "panel:class_add", "panel:class_edit", "panel:class_delete"


class ClassGroupCreateView(PanelModalFormMixin, CreateView):
    model = ClassGroup
    form_class = forms.ClassGroupForm
    title = "Add class"


class ClassGroupUpdateView(PanelModalFormMixin, UpdateView):
    model = ClassGroup
    form_class = forms.ClassGroupForm
    title = "Edit class"


class ClassGroupDeleteView(PanelModalDeleteView):
    model = ClassGroup


# --- Students (profiles auto-created with the user; edit only) ---------------------


class StudentListView(PanelListView):
    model = StudentProfile
    nav_section = "students"
    title = "Students"
    columns = (("user", "Student"), ("class_group", "Class"), ("date_of_birth", "Date of birth"))
    edit_url = "panel:student_edit"

    def get_queryset(self):
        return StudentProfile.objects.select_related("user", "class_group")


class StudentUpdateView(PanelModalFormMixin, UpdateView):
    model = StudentProfile
    form_class = forms.StudentProfileForm
    title = "Edit student"


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


class UserCreateView(PanelModalFormMixin, CreateView):
    model = User
    form_class = forms.UserCreateForm
    title = "Add user"


class UserUpdateView(PanelModalFormMixin, UpdateView):
    model = User
    form_class = forms.UserUpdateForm
    title = "Edit user"


class UserDeleteView(PanelModalDeleteView):
    model = User
