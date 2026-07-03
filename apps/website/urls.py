from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("events/", views.EventListView.as_view(), name="events"),
    path("newsletter/", views.NewsletterListView.as_view(), name="newsletter"),
    path("newsletter/<int:pk>/", views.NewsletterDetailView.as_view(), name="newsletter_detail"),
    path("gallery/", views.GalleryView.as_view(), name="gallery"),
    path("enquire/", views.EnquireView.as_view(), name="enquire"),
]
