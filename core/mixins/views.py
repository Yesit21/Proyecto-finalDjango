from django.contrib import messages
from django.shortcuts import redirect

class SuccessMessageMixin:
    success_message = ''
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

class DeleteMessageMixin:
    delete_message = 'Eliminado exitosamente'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, self.delete_message)
        return super().delete(request, *args, **kwargs)

class AjaxResponseMixin:
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)
