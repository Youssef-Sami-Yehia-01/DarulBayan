from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    # Auth
    path("login/", auth_views.LoginView.as_view(
        template_name="panel/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Dashboard
    path("", views.DashboardView.as_view(), name="dashboard"),

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

    # Users
    path("users/", views.UserListView.as_view(), name="users"),
    path("users/add/", views.UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]
