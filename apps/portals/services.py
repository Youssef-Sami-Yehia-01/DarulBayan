"""Shared query helpers for the portals."""
from django.db.models import Count, Q
from django.utils import timezone

from .models import Announcement, Homework


def student_overview(profile):
    """Context shown on a student's dashboard and on the parent's view of
    that child: upcoming homework, announcements, recent grades and an
    attendance summary keyed by status."""
    class_group = profile.class_group
    homework = (
        Homework.objects.filter(class_group=class_group, due_date__gte=timezone.localdate())
        .order_by("due_date")
        if class_group
        else Homework.objects.none()
    )
    announcements = Announcement.objects.filter(
        Q(class_group=class_group) | Q(class_group__isnull=True)
    )[:5]
    attendance_summary = dict(
        profile.attendance.values_list("status").annotate(n=Count("status"))
    )
    return {
        "profile": profile,
        "class_group": class_group,
        "upcoming_homework": homework,
        "announcements": announcements,
        "recent_grades": profile.grades.all()[:5],
        "attendance_summary": attendance_summary,
    }
