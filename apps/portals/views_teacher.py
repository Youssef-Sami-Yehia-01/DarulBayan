"""Teacher portal: my classes, rosters, attendance, homework and grades.
Every queryset is filtered to the logged-in teacher's own classes."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from apps.core.views import BaseModalDeleteView, ModalFormMixin

from . import forms
from .mixins import TeacherRequiredMixin
from .models import Announcement, Attendance, ClassGroup, Grade, Homework, StudentProfile


class TeacherDashboardView(TeacherRequiredMixin, ListView):
    template_name = "portals/teacher/dashboard.html"
    nav_section = "dashboard"
    context_object_name = "classes"

    def get_queryset(self):
        return ClassGroup.objects.filter(teacher=self.request.user).prefetch_related("students")


class TeacherClassDetailView(TeacherRequiredMixin, DetailView):
    """Roster, homework and announcements for one of my classes."""

    template_name = "portals/teacher/class_detail.html"
    nav_section = "dashboard"
    context_object_name = "class_group"

    def get_queryset(self):
        return ClassGroup.objects.filter(teacher=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            students=self.object.students.select_related("user"),
            homework=self.object.homework.all(),
            announcements=self.object.announcements.all(),
        )
        return context


class AttendanceView(TeacherRequiredMixin, TemplateView):
    """Take or edit attendance for one class on one date."""

    template_name = "portals/teacher/attendance.html"
    nav_section = "dashboard"

    def get_class_group(self):
        return get_object_or_404(
            ClassGroup, pk=self.kwargs["class_pk"], teacher=self.request.user
        )

    def get_day(self):
        return parse_date(self.request.GET.get("date", "")) or timezone.localdate()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_group = self.get_class_group()
        day = self.get_day()
        existing = {
            a.student_id: a.status
            for a in Attendance.objects.filter(class_group=class_group, date=day)
        }
        context.update(
            class_group=class_group,
            day=day,
            statuses=Attendance.Status.choices,
            rows=[
                (student, existing.get(student.pk, ""))
                for student in class_group.students.select_related("user")
            ],
        )
        return context

    def post(self, request, class_pk):
        class_group = self.get_class_group()
        day = parse_date(request.POST.get("date", ""))
        if not day:
            messages.error(request, "Pick a valid date before saving.")
            return redirect(request.path)
        for student in class_group.students.all():
            status = request.POST.get(f"status_{student.pk}")
            if status in Attendance.Status.values:
                Attendance.objects.update_or_create(
                    student=student,
                    class_group=class_group,
                    date=day,
                    defaults={"status": status},
                )
        messages.success(request, f"Attendance saved for {day:%d %b %Y}.")
        return redirect(f"{request.path}?date={day.isoformat()}")


# --- Homework (popup modals) ---------------------------------------------


class HomeworkCreateView(TeacherRequiredMixin, ModalFormMixin, CreateView):
    model = Homework
    form_class = forms.HomeworkForm
    title = "Add homework"

    def form_valid(self, form):
        form.instance.class_group = get_object_or_404(
            ClassGroup, pk=self.kwargs["class_pk"], teacher=self.request.user
        )
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class HomeworkUpdateView(TeacherRequiredMixin, ModalFormMixin, UpdateView):
    form_class = forms.HomeworkForm
    title = "Edit homework"

    def get_queryset(self):
        return Homework.objects.filter(class_group__teacher=self.request.user)


class HomeworkDeleteView(TeacherRequiredMixin, BaseModalDeleteView):
    def get_queryset(self):
        return Homework.objects.filter(class_group__teacher=self.request.user)


# --- Grades (popup modals) -------------------------------------------------


class StudentGradesView(TeacherRequiredMixin, DetailView):
    """All grades of one student in my classes."""

    template_name = "portals/teacher/student_grades.html"
    nav_section = "dashboard"
    context_object_name = "student"

    def get_queryset(self):
        return StudentProfile.objects.filter(
            class_group__teacher=self.request.user
        ).select_related("user", "class_group")


class GradeCreateView(TeacherRequiredMixin, ModalFormMixin, CreateView):
    model = Grade
    form_class = forms.GradeForm
    title = "Add grade"

    def form_valid(self, form):
        form.instance.student = get_object_or_404(
            StudentProfile,
            pk=self.kwargs["student_pk"],
            class_group__teacher=self.request.user,
        )
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class GradeUpdateView(TeacherRequiredMixin, ModalFormMixin, UpdateView):
    form_class = forms.GradeForm
    title = "Edit grade"

    def get_queryset(self):
        return Grade.objects.filter(student__class_group__teacher=self.request.user)


class GradeDeleteView(TeacherRequiredMixin, BaseModalDeleteView):
    def get_queryset(self):
        return Grade.objects.filter(student__class_group__teacher=self.request.user)


# --- Class announcements (popup modals) --------------------------------------


class AnnouncementCreateView(TeacherRequiredMixin, ModalFormMixin, CreateView):
    model = Announcement
    form_class = forms.AnnouncementForm
    title = "Add announcement"

    def form_valid(self, form):
        form.instance.class_group = get_object_or_404(
            ClassGroup, pk=self.kwargs["class_pk"], teacher=self.request.user
        )
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AnnouncementDeleteView(TeacherRequiredMixin, BaseModalDeleteView):
    def get_queryset(self):
        return Announcement.objects.filter(class_group__teacher=self.request.user)
