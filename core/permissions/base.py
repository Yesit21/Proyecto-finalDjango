from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = []
    
    def test_func(self):
        return self.request.user.rol in self.required_roles

class AdminRequiredMixin(RoleRequiredMixin):
    required_roles = ['administrador']

class MeseroRequiredMixin(RoleRequiredMixin):
    required_roles = ['mesero', 'administrador']

class ClienteRequiredMixin(RoleRequiredMixin):
    required_roles = ['cliente']
