from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.utils import timezone

from roles.mixins import StaffPermissionRequiredMixin, StaffHeaderMixin, StaffListingMixin
from products.models import Product
from accounts.models import Address
from accounts.forms import AddressForm
from .models import Order, OrderDetail, Delivery, Rating, Payment
from . import selectors, services
from .cart import Cart


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('products:product_catalog')
            
        addresses = request.user.addresses.all()
        address_form = AddressForm()
        
        return render(request, self.template_name, {
            'cart': cart,
            'addresses': addresses,
            'address_form': address_form,
            'payment_methods': Payment.PAYMENT_METHOD_CHOICES
        })

    def post(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return redirect('products:product_catalog')

        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method', 'card')
        address = None
        
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
        else:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
            else:
                addresses = request.user.addresses.all()
                return render(request, self.template_name, {
                    'cart': cart,
                    'addresses': addresses,
                    'address_form': address_form,
                    'payment_methods': Payment.PAYMENT_METHOD_CHOICES
                })

        try:
            services.process_checkout(
                user=request.user,
                cart=cart,
                address=address,
                payment_method=payment_method
            )
            cart.clear()
            messages.success(request, "¡Pedido y envío generados con éxito!")
            return redirect('home')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('orders:checkout')
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar tu pedido: {str(e)}")
            return redirect('orders:checkout')


class OrderListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, ListView):
    model = Order
    template_name = 'staff/orders/order_list.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    header_title = "Gestión de Pedidos"
    header_subtitle = "Control Maestro de Ventas y Estado"
    count_label = "Total Pedidos"

    def get_queryset(self):
        return selectors.get_all_orders()

class OrderDetailView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, DetailView):
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

class DeliveryListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, ListView):
    model = Delivery
    template_name = 'staff/orders/delivery_list.html'
    context_object_name = 'deliveries'
    permission_required = 'orders.view_delivery'
    header_title = "Gestión de Entregas"
    header_subtitle = "Seguimiento y Logística de Envío"
    count_label = "Total Despachos"

    def get_queryset(self):
        return selectors.get_all_deliveries()

class RatingListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, ListView):
    model = Rating
    template_name = 'staff/orders/rating_list.html'
    context_object_name = 'ratings'
    permission_required = 'orders.view_rating'
    header_title = "Calificaciones"
    header_subtitle = "Feedback y Experiencia del Cliente"
    count_label = "Total Valoraciones"

    def get_queryset(self):
        return selectors.get_all_ratings()

class PaymentListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, ListView):
    model = Payment
    template_name = 'staff/orders/payment_list.html'
    context_object_name = 'payments'
    permission_required = 'orders.view_payment'
    header_title = "Gestión de Pagos"
    header_subtitle = "Monitoreo de Transacciones y Finanzas"
    count_label = "Total Pagos"

    def get_queryset(self):
        return selectors.get_all_payments()
class UpdateDeliveryStatusView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'orders.change_delivery'

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            services.update_order_status(order, new_status)
            messages.success(request, f"Estado del pedido #{order.id} actualizado a {new_status}.")
        else:
            messages.error(request, "Estado no válido.")
        return redirect('orders:delivery_list')



class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        override = request.POST.get('override', 'False').lower() == 'true'
        cart.add(product=product, quantity=quantity, override_quantity=override)
        
        if request.headers.get('HX-Request'):
            return render(request, 'orders/cart_modal_partial.html', {'cart': cart})
        return redirect('products:product_catalog')

class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        
        if request.headers.get('HX-Request'):
            return render(request, 'orders/cart_modal_partial.html', {'cart': cart})
        return redirect('products:product_catalog')

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart_modal_partial.html', {'cart': cart})