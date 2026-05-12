from django.db.models import ProtectedError
from django.views.generic import ListView, DetailView, UpdateView, View
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from roles.mixins import StaffPermissionRequiredMixin, StaffHeaderMixin, StaffListingMixin, StaffPaginationMixin
from products.models import Product
from .models import Order, OrderDetail, Delivery, Rating
from accounts.models import Address, Municipality
from accounts.forms import AddressForm
from . import selectors, services
from base.models import SiteParameter
from .cart import Cart

OrderDetailFormSet = inlineformset_factory(
    Order, OrderDetail, 
    fields=('quantity',), 
    extra=0, 
    can_delete=True,
    widgets={
        'quantity': forms.NumberInput(attrs={
            'class': 'bg-gray-50 border border-gray-100 text-gray-900 text-sm font-black rounded-xl block w-full p-3 focus:ring-orange-500 focus:border-orange-500',
            'min': '1'
        })
    }
)

class StaffOrderEditView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, UpdateView):
    model = Order
    template_name = 'staff/orders/order_edit.html'
    fields = [] # We use formset instead
    permission_required = 'orders.change_order'
    header_title = "Editar Pedido"
    header_subtitle = "Ajustar cantidades de productos"
    header_show_back = True

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderDetailFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderDetailFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            
            # Recalculate total
            total = 0
            for detail in self.object.details.all():
                detail.subtotal = detail.quantity * detail.unit_price
                detail.save()
                total += detail.subtotal
            self.object.total = total
            self.object.save()
            
            messages.success(self.request, "Pedido actualizado correctamente.")
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('products:product_catalog')
            
        addresses = request.user.addresses.all()
        address_form = AddressForm()
        municipalities = Municipality.objects.all()
        
        return render(request, self.template_name, {
            'cart': cart,
            'addresses': addresses,
            'address_form': address_form,
            'municipalities': municipalities
        })

    def post(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return redirect('products:product_catalog')

        address_id = request.POST.get('address_id')
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
                municipalities = Municipality.objects.all()
                return render(request, self.template_name, {
                    'cart': cart,
                    'addresses': addresses,
                    'address_form': address_form,
                    'municipalities': municipalities
                })

        try:
            order = services.process_checkout(
                user=request.user,
                cart=cart,
                address=address
            )
            
            # WhatsApp Redirection Logic
            phone_param = SiteParameter.objects.filter(key='CONTACT_PHONE').first()
            phone = phone_param.value if phone_param else '573000000000' # Fallback
            
            # Clean phone number (remove non-digits)
            phone = ''.join(filter(str.isdigit, phone))
            
            message = f"🍔 *NUEVO PEDIDO - KOKORI BROASTER*\n"
            message += f"----------------------------------\n"
            message += f"🆔 *Orden*: #{order.id}\n"
            message += f"👤 *Cliente*: {request.user.get_full_name() or request.user.username}\n"
            message += f"📍 *Dirección*: {address.street}, {address.neighborhood}\n"
            message += f"----------------------------------\n"
            message += f"🛒 *Productos*:\n"
            for detail in order.details.all():
                message += f"- {detail.product.name} x{detail.quantity} (${detail.subtotal})\n"
            message += f"----------------------------------\n"
            message += f"💰 *TOTAL A PAGAR*: ${order.total}\n\n"
            message += f"✅ Por favor, confírmame el pedido para iniciar la preparación."
            
            import urllib.parse
            whatsapp_url = f"https://api.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}"
            
            cart.clear()
            return render(request, 'orders/checkout_success.html', {
                'whatsapp_url': whatsapp_url,
                'order': order
            })

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('orders:checkout')
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar tu pedido: {str(e)}")
            return redirect('orders:checkout')


class OrderListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = Order
    template_name = 'staff/orders/order_list.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    paginate_by = 10
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
    header_subtitle = "Información Completa del Pedido"
    header_show_back = True
    header_back_url = reverse_lazy('orders:order_list')

    def get_object(self):
        return selectors.get_order_by_id(self.kwargs.get('pk'))

class DeliveryListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = Delivery
    template_name = 'staff/orders/delivery_list.html'
    context_object_name = 'deliveries'
    permission_required = 'orders.view_delivery'
    paginate_by = 10
    header_title = "Gestión de Entregas"
    header_subtitle = "Seguimiento y Logística de Envío"
    count_label = "Total Despachos"

    def get_queryset(self):
        return selectors.get_all_deliveries()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contar pedidos que NO están en estado 'shipped', 'delivered' o 'cancelled'
        active_deliveries_count = Order.objects.exclude(status__in=['shipped', 'delivered', 'cancelled']).count()
        context['header_config']['count_value'] = active_deliveries_count
        return context

class RatingListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = Rating
    template_name = 'staff/orders/rating_list.html'
    context_object_name = 'ratings'
    permission_required = 'orders.view_rating'
    paginate_by = 10
    header_title = "Calificaciones"
    header_subtitle = "Feedback y Experiencia del Cliente"
    count_label = "Total Valoraciones"

    def get_queryset(self):
        return selectors.get_all_ratings()

class UpdateDeliveryStatusView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'orders.change_delivery'

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            try:
                services.update_order_status(order, new_status)
                messages.success(request, f"Estado del pedido #{order.id} actualizado a {new_status}.")
            except ValueError as e:
                messages.error(request, str(e))
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

class RatingCreateView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user, status='delivered')
        if Rating.objects.filter(order=order).exists():
            messages.error(request, "Ya has calificado este pedido.")
            return redirect('accounts:my_orders')
            
        try:
            score = int(request.POST.get('score', 0))
        except ValueError:
            score = 0
            
        comment = request.POST.get('comment', '')
        
        if 1 <= score <= 5:
            Rating.objects.create(user=request.user, order=order, score=score, comment=comment)
            messages.success(request, "¡Gracias por tu calificación!")
        else:
            messages.error(request, "Puntuación inválida.")
            
        return redirect('accounts:my_orders')

class RatingUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        rating = get_object_or_404(Rating, id=pk, user=request.user)
        try:
            score = int(request.POST.get('score', 0))
        except ValueError:
            score = 0
            
        comment = request.POST.get('comment', '')
        
        if 1 <= score <= 5:
            rating.score = score
            rating.comment = comment
            rating.save()
            messages.success(request, "Calificación actualizada exitosamente.")
        else:
            messages.error(request, "Puntuación inválida.")
            
        return redirect('accounts:my_orders')

class RatingDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        rating = get_object_or_404(Rating, id=pk, user=request.user)
        rating.delete()
        messages.success(request, "Calificación eliminada.")
        return redirect('accounts:my_orders')

class StaffRatingDeleteView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'orders.delete_rating'
    
    def post(self, request, pk):
        rating = get_object_or_404(Rating, id=pk)
        rating.delete()
        messages.success(request, "Calificación eliminada exitosamente por el staff.")
        referer = request.META.get('HTTP_REFERER', '')
        if referer and url_has_allowed_host_and_scheme(
            referer,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(referer)
        return redirect('orders:rating_list')


# --- Municipality Management ---

class MunicipalityListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = Municipality
    template_name = 'staff/orders/municipality_list.html'
    context_object_name = 'municipalities'
    permission_required = 'accounts.view_municipality'
    paginate_by = 10
    ordering = ['name']
    header_title = "Municipios"
    header_subtitle = "Gestión de Territorios y Cobertura"
    count_label = "Total Municipios"



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_municipality_create_url'] = reverse_lazy('orders:municipality_create')
        return context

class MunicipalityCreateView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'accounts.add_municipality'

    def post(self, request):
        name = request.POST.get('name')
        code = request.POST.get('code')
        if name and code:
            Municipality.objects.create(name=name, code=code)
            messages.success(request, f"Municipio '{name}' creado.")
        else:
            messages.error(request, "Nombre y código son obligatorios.")
        return redirect('orders:municipality_list')

class MunicipalityUpdateView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'accounts.change_municipality'

    def post(self, request, pk):
        m = get_object_or_404(Municipality, id=pk)
        name = request.POST.get('name')
        code = request.POST.get('code')
        if name and code:
            m.name = name
            m.code = code
            m.save()
            messages.success(request, f"Municipio '{name}' actualizado.")
        else:
            messages.error(request, "Nombre y código son obligatorios.")
        return redirect('orders:municipality_list')

class MunicipalityDeleteView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'accounts.delete_municipality'

    def post(self, request, pk):
        m = get_object_or_404(Municipality, id=pk)
        name = m.name
        try:
            m.delete()
            messages.success(request, f"Municipio '{name}' eliminado.")
        except ProtectedError:
            messages.error(request, f"No se puede eliminar '{name}' porque tiene direcciones asociadas.")
        return redirect('orders:municipality_list')