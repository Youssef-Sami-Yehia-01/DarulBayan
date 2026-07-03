from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class PostLoginRedirectView(LoginRequiredMixin, View):
    """Sends each user to their area right after login:
    staff/management -> admin panel, otherwise their role portal."""

    def get(self, request):
        user = request.user
        if user.is_staff or user.is_management:
            return redirect("panel:dashboard")
        if user.is_teacher:
            return redirect("portals:teacher_dashboard")
        if user.is_parent:
            return redirect("portals:parent_dashboard")
        return redirect("portals:student_dashboard")
