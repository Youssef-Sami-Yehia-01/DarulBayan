from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    # Dashboard
    path("", views.DashboardView.as_view(), name="dashboard"),

    # Info pages + content blocks
    path("pages/", views.InfoPageListView.as_view(), name="pages"),
    path("pages/add/", views.InfoPageCreateView.as_view(), name="page_add"),
    path("pages/<int:pk>/edit/", views.InfoPageUpdateView.as_view(), name="page_edit"),
    path("pages/<int:pk>/delete/", views.InfoPageDeleteView.as_view(), name="page_delete"),
    path("pages/<int:pk>/blocks/", views.ContentBlockListView.as_view(), name="page_blocks"),
    path("pages/<int:page_pk>/blocks/add/", views.ContentBlockCreateView.as_view(), name="block_add"),
    path("blocks/<int:pk>/edit/", views.ContentBlockUpdateView.as_view(), name="block_edit"),
    path("blocks/<int:pk>/delete/", views.ContentBlockDeleteView.as_view(), name="block_delete"),

    # Events
    path("events/", views.EventListView.as_view(), name="events"),
    path("events/add/", views.EventCreateView.as_view(), name="event_add"),
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_edit"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),

    # Newsletter
    path("newsletter/", views.NewsletterListView.as_view(), name="newsletter"),
    path("newsletter/add/", views.NewsletterCreateView.as_view(), name="post_add"),
    path("newsletter/<int:pk>/edit/", views.NewsletterUpdateView.as_view(), name="post_edit"),
    path("newsletter/<int:pk>/delete/", views.NewsletterDeleteView.as_view(), name="post_delete"),

    # Gallery images + categories
    path("gallery/", views.GalleryListView.as_view(), name="gallery"),
    path("gallery/add/", views.GalleryImageCreateView.as_view(), name="image_add"),
    path("gallery/<int:pk>/edit/", views.GalleryImageUpdateView.as_view(), name="image_edit"),
    path("gallery/<int:pk>/delete/", views.GalleryImageDeleteView.as_view(), name="image_delete"),
    path("gallery/categories/", views.GalleryCategoryListView.as_view(), name="categories"),
    path("gallery/categories/add/", views.GalleryCategoryCreateView.as_view(), name="category_add"),
    path("gallery/categories/<int:pk>/edit/", views.GalleryCategoryUpdateView.as_view(), name="category_edit"),
    path("gallery/categories/<int:pk>/delete/", views.GalleryCategoryDeleteView.as_view(), name="category_delete"),

    # Enquiries
    path("enquiries/", views.EnquiryListView.as_view(), name="enquiries"),
    path("enquiries/<int:pk>/", views.EnquiryDetailView.as_view(), name="enquiry_detail"),
    path("enquiries/<int:pk>/toggle/", views.EnquiryToggleHandledView.as_view(), name="enquiry_toggle"),
    path("enquiries/<int:pk>/delete/", views.EnquiryDeleteView.as_view(), name="enquiry_delete"),

    # Announcements
    path("announcements/", views.AnnouncementListView.as_view(), name="announcements"),
    path("announcements/add/", views.AnnouncementCreateView.as_view(), name="announcement_add"),
    path("announcements/<int:pk>/edit/", views.AnnouncementUpdateView.as_view(), name="announcement_edit"),
    path("announcements/<int:pk>/delete/", views.AnnouncementDeleteView.as_view(), name="announcement_delete"),

    # Classes
    path("classes/", views.ClassGroupListView.as_view(), name="classes"),
    path("classes/add/", views.ClassGroupCreateView.as_view(), name="class_add"),
    path("classes/<int:pk>/edit/", views.ClassGroupUpdateView.as_view(), name="class_edit"),
    path("classes/<int:pk>/delete/", views.ClassGroupDeleteView.as_view(), name="class_delete"),

    # Students
    path("students/", views.StudentListView.as_view(), name="students"),
    path("students/<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_edit"),

    # Users
    path("users/", views.UserListView.as_view(), name="users"),
    path("users/add/", views.UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]
