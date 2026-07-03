"""Student portal: read-only view of my class, homework, grades, attendance.
The StudentProfile always exists (created by signals.py)."""
from django.views.generic import ListView, TemplateView

from .mixins import StudentRequiredMixin
from .models import Homework
from .services import student_overview


class StudentDashboardView(StudentRequiredMixin, TemplateView):
    template_name = "portals/student/dashboard.html"
    nav_section = "dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(student_overview(self.request.user.student_profile))
        return context


class StudentHomeworkView(StudentRequiredMixin, ListView):
    template_name = "portals/student/homework.html"
    nav_section = "homework"
    paginate_by = 10

    def get_queryset(self):
        class_group = self.request.user.student_profile.class_group
        if not class_group:
            return Homework.objects.none()
        return class_group.homework.all()


class StudentGradesView(StudentRequiredMixin, ListView):
    template_name = "portals/student/grades.html"
    nav_section = "grades"
    paginate_by = 15

    def get_queryset(self):
        return self.request.user.student_profile.grades.all()


class StudentAttendanceView(StudentRequiredMixin, ListView):
    template_name = "portals/student/attendance.html"
    nav_section = "attendance"
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.student_profile.attendance.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attendance_summary"] = student_overview(
            self.request.user.student_profile
        )["attendance_summary"]
        return context
