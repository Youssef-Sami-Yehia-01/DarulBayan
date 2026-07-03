"""Generic building blocks for popup-modal CRUD, reused by the admin
panel and the portals.

Modal protocol (see static/js/modal.js):
  GET  -> HTML fragment (form or confirmation) rendered inside the modal
  POST -> 204 on success (modal.js then reloads the page)
          400 + re-rendered fragment when validation fails
"""
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.views.generic import DeleteView


class ModalFormMixin:
    """Mix into a CreateView/UpdateView opened inside the popup modal.
    Combine with an access mixin (staff/role check) in the concrete view."""

    template_name = "components/modal_form.html"
    title = ""

    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=400)


class BaseModalDeleteView(DeleteView):
    """Delete confirmation opened inside the popup modal.
    Combine with an access mixin (staff/role check) in the concrete view."""

    template_name = "components/modal_delete.html"

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                error="This item is still used by other content and cannot be deleted."
            )
            return self.render_to_response(context, status=400)
        return HttpResponse(status=204)
