"""View mixins shared across apps."""


class NavSectionMixin:
    """Exposes `nav_active` to templates so navigation components can
    highlight the current section. Set `nav_section` on the view."""

    nav_section = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_active"] = self.nav_section
        return context
