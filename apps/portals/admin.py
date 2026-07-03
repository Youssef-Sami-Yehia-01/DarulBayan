"""Django admin registration — technical fallback only; teachers and the
/panel/ app are the primary way to manage these records."""
from django.contrib import admin

from .models import Announcement, Attendance, ClassGroup, Grade, Homework, StudentProfile

admin.site.register(ClassGroup)
admin.site.register(StudentProfile)
admin.site.register(Attendance)
admin.site.register(Homework)
admin.site.register(Grade)
admin.site.register(Announcement)
