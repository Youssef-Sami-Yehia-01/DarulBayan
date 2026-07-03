"""Template helpers shared across the project."""
from django import template

register = template.Library()


@register.filter
def field_value(obj, field):
    """Human-friendly value of `field` on `obj` for the generic panel
    tables: uses get_<field>_display for choice fields and Yes/No for
    booleans; other values render as-is."""
    display = getattr(obj, f"get_{field}_display", None)
    if callable(display):
        return display()
    value = getattr(obj, field)
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return value
