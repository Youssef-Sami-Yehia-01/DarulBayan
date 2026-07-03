"""Academic records behind the student/parent/teacher portals."""
from django.conf import settings
from django.db import models


class ClassGroup(models.Model):
    """A class of students taught by one teacher."""

    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "teacher"},
        related_name="classes",
    )
    schedule = models.CharField(
        max_length=200, blank=True, help_text="e.g. Saturdays 10:00–12:00"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    """Academic profile attached to every user with the student role
    (created automatically by signals.py)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile"
    )
    class_group = models.ForeignKey(
        ClassGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="students"
    )
    parents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        limit_choices_to={"role": "parent"},
        related_name="children",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Visible to staff and teachers only.")

    class Meta:
        ordering = ["user__first_name", "user__username"]

    def __str__(self):
        return str(self.user)


class Attendance(models.Model):
    """One student's attendance mark for one class session date."""

    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        LATE = "late", "Late"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendance")
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "class_group", "date"], name="unique_attendance_mark"
            )
        ]

    def __str__(self):
        return f"{self.student} — {self.date} — {self.get_status_display()}"


class Homework(models.Model):
    """Assignment set by a teacher for a whole class."""

    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="homework")
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    due_date = models.DateField()
    attachment = models.FileField(upload_to="homework/", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-due_date"]
        verbose_name_plural = "homework"

    def __str__(self):
        return self.title


class Grade(models.Model):
    """A mark a teacher records for one student."""

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grades")
    title = models.CharField(max_length=200, help_text="e.g. Term 1 reading assessment")
    score = models.DecimalField(max_digits=6, decimal_places=2)
    max_score = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    date = models.DateField()
    feedback = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+"
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title}: {self.score}/{self.max_score}"


class Announcement(models.Model):
    """Message to a class, or to the whole school when class_group is empty."""

    title = models.CharField(max_length=200)
    body = models.TextField()
    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="announcements",
        help_text="Leave empty to address the whole school.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
