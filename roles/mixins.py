from django.contrib.auth.mixins import PermissionRequiredMixin

class RolePermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        user = self.request.user
        return user.is_authenticated and super().has_permission()

class StaffPermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff and super().has_permission()

class StaffHeaderMixin:
    """Mixin to provide context for the standardized admin header."""
    header_title = ""
    header_subtitle = ""
    header_cta_label = None
    header_cta_url = None
    header_cta_onclick = None
    header_back_url = None
    header_show_back = False

    def get_context_data(self, **kwargs):
        if hasattr(super(), 'get_context_data'):
            context = super().get_context_data(**kwargs)
        else:
            context = kwargs.copy()
            
        context['header_config'] = {
            'title': self.header_title,
            'subtitle': self.header_subtitle,
            'cta_label': self.header_cta_label,
            'cta_url': self.header_cta_url,
            'cta_onclick': self.header_cta_onclick,
            'back_url': self.header_back_url,
            'show_back': self.header_show_back,
        }
        return context

class StaffListingMixin(StaffHeaderMixin):
    """Specific mixin for list views that includes count stats."""
    count_label = "Total Registros"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Try to get count from object_list or queryset
        object_list = context.get('object_list')
        if object_list is not None:
            context['header_config']['count_value'] = object_list.count()
            context['header_config']['count_label'] = self.count_label
        return context
