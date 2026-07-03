"""Access control for the role portals."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from apps.core.mixins import NavSectionMixin


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin, NavSectionMixin):
    """Restricts a portal view to one user role."""

    required_role = ""

    def test_func(self):
        return self.request.user.role == self.required_role


class TeacherRequiredMixin(RoleRequiredMixin):
    required_role = "teacher"


class StudentRequiredMixin(RoleRequiredMixin):
    required_role = "student"


class ParentRequiredMixin(RoleRequiredMixin):
    required_role = "parent"
