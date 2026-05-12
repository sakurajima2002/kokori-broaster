from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from accounts.models import User
from .forms import GroupForm, UserRoleForm
from .mixins import StaffListingMixin, StaffHeaderMixin, StaffPermissionRequiredMixin, StaffPaginationMixin

class GroupListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = Group
    template_name = 'staff/roles/group_list.html'
    context_object_name = 'groups'
    permission_required = 'auth.view_group'
    paginate_by = 10
    ordering = ['name']
    header_title = "Roles y Permisos"
    header_subtitle = "Configuración de Niveles de Acceso"
    header_cta_label = "Nuevo Rol"
    header_cta_url = reverse_lazy('roles:group_create')
    count_label = "Roles Definidos"

class GroupCreateView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'staff/roles/group_form.html'
    success_url = reverse_lazy('roles:group_list')
    permission_required = 'auth.add_group'
    header_title = "Crear Rol"
    header_subtitle = "Definición de Nuevo Perfil de Staff"
    header_show_back = True
    header_back_url = reverse_lazy('roles:group_list')

    def form_valid(self, form):
        messages.success(self.request, f'Rol "{form.cleaned_data["name"]}" creado con éxito.')
        return super().form_valid(form)

class GroupUpdateView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'staff/roles/group_form.html'
    success_url = reverse_lazy('roles:group_list')
    permission_required = 'auth.change_group'
    header_title = "Editar Rol"
    header_subtitle = "Actualización de Permisos y Nombre"
    header_show_back = True
    header_back_url = reverse_lazy('roles:group_list')

    def form_valid(self, form):
        messages.success(self.request, f'Rol "{form.cleaned_data["name"]}" actualizado con éxito.')
        return super().form_valid(form)

class GroupDeleteView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, DeleteView):
    model = Group
    template_name = 'staff/roles/group_confirm_delete.html'
    success_url = reverse_lazy('roles:group_list')
    permission_required = 'auth.delete_group'
    header_title = "Eliminar Rol"
    header_subtitle = "Confirmación de Borrado Permanente"
    header_show_back = True
    header_back_url = reverse_lazy('roles:group_list')

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        messages.success(self.request, f'Rol "{group.name}" eliminado.')
        return super().delete(request, *args, **kwargs)

class UserRoleUpdateView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, UpdateView):
    model = User
    form_class = UserRoleForm
    template_name = 'staff/roles/user_role_form.html'
    success_url = reverse_lazy('accounts:user_list')
    permission_required = 'accounts.change_user'
    header_title = "Asignación de Roles"
    header_subtitle = "Gestión de Permisos Individuales"
    header_show_back = True
    header_back_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, f'Roles de "{self.object.email}" actualizados.')
        return super().form_valid(form)