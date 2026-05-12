from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from roles.mixins import StaffPermissionRequiredMixin, StaffListingMixin, StaffHeaderMixin, StaffPaginationMixin
from .models import SiteParameter

class SiteParameterListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = SiteParameter
    template_name = 'staff/configuration/parameter_list.html'
    context_object_name = 'parameters'
    permission_required = 'base.view_siteparameter'
    paginate_by = 10
    header_title = "Parámetros Globales"
    header_subtitle = "Configuración General del Sitio"
    count_label = "Total Parámetros"

    def get_queryset(self):
        return SiteParameter.objects.all()

class SiteParameterUpdateView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, UpdateView):
    model = SiteParameter
    template_name = 'staff/configuration/parameter_form.html'
    fields = ['value', 'image']
    success_url = reverse_lazy('base:parameter_list')
    permission_required = 'base.change_siteparameter'
    header_title = "Editar Parámetro"
    header_subtitle = "Actualización de Configuración"
    header_show_back = True
    header_back_url = reverse_lazy('base:parameter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parameter'] = self.get_object()
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Parámetro '{self.get_object().label}' actualizado correctamente.")
        return super().form_valid(form)
