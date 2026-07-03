from django.urls import path

from . import views_parent, views_student, views_teacher

app_name = "portals"

urlpatterns = [
    # Teacher
    path("teacher/", views_teacher.TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("teacher/class/<int:pk>/", views_teacher.TeacherClassDetailView.as_view(), name="teacher_class"),
    path("teacher/class/<int:class_pk>/attendance/", views_teacher.AttendanceView.as_view(), name="teacher_attendance"),
    path("teacher/class/<int:class_pk>/homework/add/", views_teacher.HomeworkCreateView.as_view(), name="homework_add"),
    path("teacher/homework/<int:pk>/edit/", views_teacher.HomeworkUpdateView.as_view(), name="homework_edit"),
    path("teacher/homework/<int:pk>/delete/", views_teacher.HomeworkDeleteView.as_view(), name="homework_delete"),
    path("teacher/class/<int:class_pk>/announcement/add/", views_teacher.AnnouncementCreateView.as_view(), name="announcement_add"),
    path("teacher/announcement/<int:pk>/delete/", views_teacher.AnnouncementDeleteView.as_view(), name="announcement_delete"),
    path("teacher/student/<int:pk>/grades/", views_teacher.StudentGradesView.as_view(), name="teacher_student_grades"),
    path("teacher/student/<int:student_pk>/grades/add/", views_teacher.GradeCreateView.as_view(), name="grade_add"),
    path("teacher/grade/<int:pk>/edit/", views_teacher.GradeUpdateView.as_view(), name="grade_edit"),
    path("teacher/grade/<int:pk>/delete/", views_teacher.GradeDeleteView.as_view(), name="grade_delete"),

    # Student
    path("student/", views_student.StudentDashboardView.as_view(), name="student_dashboard"),
    path("student/homework/", views_student.StudentHomeworkView.as_view(), name="student_homework"),
    path("student/grades/", views_student.StudentGradesView.as_view(), name="student_grades"),
    path("student/attendance/", views_student.StudentAttendanceView.as_view(), name="student_attendance"),

    # Parent
    path("parent/", views_parent.ParentDashboardView.as_view(), name="parent_dashboard"),
    path("parent/child/<int:pk>/", views_parent.ChildDetailView.as_view(), name="parent_child"),
]
