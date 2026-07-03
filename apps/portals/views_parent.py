"""Parent portal: read-only overview of each linked child."""
from django.views.generic import DetailView, ListView

from .mixins import ParentRequiredMixin
from .models import StudentProfile
from .services import student_overview


class ParentDashboardView(ParentRequiredMixin, ListView):
    template_name = "portals/parent/dashboard.html"
    nav_section = "children"
    context_object_name = "children"

    def get_queryset(self):
        return StudentProfile.objects.filter(parents=self.request.user).select_related(
            "user", "class_group"
        )


class ChildDetailView(ParentRequiredMixin, DetailView):
    """One child's homework, grades and attendance. Only reachable for
    children actually linked to the logged-in parent."""

    template_name = "portals/parent/child_detail.html"
    nav_section = "children"
    context_object_name = "child"

    def get_queryset(self):
        return StudentProfile.objects.filter(parents=self.request.user).select_related(
            "user", "class_group"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(student_overview(self.object))
        return context
