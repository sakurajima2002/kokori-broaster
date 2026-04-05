from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from roles.mixins import RolePermissionRequiredMixin, StaffHeaderMixin, StaffListingMixin
from .models import Order, Delivery, Rating
from . import selectors

class OrderListView(LoginRequiredMixin, RolePermissionRequiredMixin, StaffListingMixin, ListView):
    model = Order
    template_name = 'staff/orders/order_list.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    header_title = "Gestión de Pedidos"
    header_subtitle = "Control Maestro de Ventas y Estado"
    count_label = "Total Pedidos"

    def get_queryset(self):
        return selectors.get_all_orders()

class OrderDetailView(LoginRequiredMixin, RolePermissionRequiredMixin, StaffHeaderMixin, DetailView):
    model = Order
    template_name = 'staff/orders/order_detail.html'
    context_object_name = 'order'
    permission_required = 'orders.view_order'
    header_title = "Detalle del Pedido"
    header_subtitle = "Información Completa y Transacciones"
    header_show_back = True
    header_back_url = reverse_lazy('orders:order_list')

    def get_object(self):
        return selectors.get_order_by_id(self.kwargs.get('pk'))

class DeliveryListView(LoginRequiredMixin, RolePermissionRequiredMixin, StaffListingMixin, ListView):
    model = Delivery
    template_name = 'staff/orders/delivery_list.html'
    context_object_name = 'deliveries'
    permission_required = 'orders.view_delivery'
    header_title = "Gestión de Entregas"
    header_subtitle = "Seguimiento y Logística de Envío"
    count_label = "Total Despachos"

    def get_queryset(self):
        return selectors.get_all_deliveries()

class RatingListView(LoginRequiredMixin, RolePermissionRequiredMixin, StaffListingMixin, ListView):
    model = Rating
    template_name = 'staff/orders/rating_list.html'
    context_object_name = 'ratings'
    permission_required = 'orders.view_rating'
    header_title = "Calificaciones"
    header_subtitle = "Feedback y Experiencia del Cliente"
    count_label = "Total Valoraciones"

    def get_queryset(self):
        return selectors.get_all_ratings()
