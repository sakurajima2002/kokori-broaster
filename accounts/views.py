from roles.mixins import StaffListingMixin, StaffHeaderMixin, StaffPermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import User, Address
from .forms import LoginUserForm, RegisterUserForm
from products.models import Product
from orders.models import Order
from django.db.models import Sum

class LoginUserView(View):
    template_login = 'users/accounts/login.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_login, {'form': LoginUserForm})
    
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        messages.warning(request, 'El usuario o la contraseña no son válidos!')
        return render(request, self.template_login, context={'form': form})

class RegisterUserView(View):
    template_register = 'users/accounts/register.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_register, {'form': RegisterUserForm})
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        messages.warning(request, 'El usuario o la contraseña no son válidos!')
        return render(request, self.template_register, context={'form': form})

class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')

class HomeView(StaffHeaderMixin, View):
    header_title = "Panel de Control"
    header_subtitle = "Visión General y Métricas de Rendimiento"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            # Metrics
            try:
                threshold = int(request.GET.get('stock_threshold', 5))
                if threshold < 0: threshold = 0
            except (ValueError, TypeError):
                threshold = 5
                
            total_users = User.objects.count()
            total_products = Product.objects.count()
            low_stock_products = Product.objects.filter(stock__lte=threshold).order_by('stock')
            low_stock_count = low_stock_products.count()
            
            total_orders = Order.objects.count()
            pending_orders_count = Order.objects.filter(status='pending').count()
            
            total_sales = Order.objects.filter(
                status__in=['paid', 'delivered']
            ).aggregate(Sum('total'))['total__sum'] or 0
            
            recent_orders = Order.objects.all().order_by('-order_date')[:5]

            context = self.get_context_data()
            context.update({
                'total_users': total_users,
                'total_products': total_products,
                'low_stock_products': low_stock_products,
                'low_stock_count': low_stock_count,
                'total_orders': total_orders,
                'pending_orders_count': pending_orders_count,
                'total_sales': total_sales,
                'recent_orders': recent_orders,
                'stock_threshold': threshold,
            })
            return render(request, 'staff/dashboard.html', context)
        return render(request, 'users/home.html')

class UserListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, ListView):
    model = User
    template_name = 'staff/accounts/user_list.html'
    context_object_name = 'users'
    permission_required = 'accounts.view_user'
    header_title = "Gestión de Usuarios"
    header_subtitle = "Control de Acceso y Perfiles de Staff"
    count_label = "Usuarios Registrados"

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user.id)

class UserDetailView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, DetailView):
    model = User
    template_name = 'staff/accounts/user_detail.html'
    context_object_name = 'user'
    permission_required = 'accounts.view_user'
    header_title = "Perfil de Usuario"
    header_subtitle = "Detalles de Cuenta y Actividad"
    header_show_back = True
    header_back_url = reverse_lazy('accounts:user_list')

class UserStaffStatusToggleView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'accounts.change_user'

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        if user == request.user:
            messages.error(request, "No puedes cambiar tu propio estado de staff.")
            return redirect('accounts:user_list')
            
        user.is_staff = not user.is_staff
        user.save()
        
        status_text = "ahora es Staff" if user.is_staff else "ya no es Staff"
        messages.success(request, f'El usuario {user.email} {status_text}.')
        return redirect('accounts:user_list')

class AddressListView(LoginRequiredMixin, StaffPermissionRequiredMixin, ListView):
    model = Address
    template_name = 'users/accounts/address_list.html'
    context_object_name = 'addresses'
    permission_required = 'accounts.view_address'

class AddressDetailView(LoginRequiredMixin, StaffPermissionRequiredMixin, DetailView):
    model = Address
    template_name = 'users/accounts/address_detail.html'
    context_object_name = 'address'
    permission_required = 'accounts.view_address'