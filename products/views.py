from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View

from roles.mixins import StaffPermissionRequiredMixin, StaffHeaderMixin, StaffListingMixin, StaffPaginationMixin
from .models import Category, Product
from .forms import ProductForm, CategoryForm, ComboDetailFormSet
from . import selectors




class ProductCatalogView(View):
    template_name = 'products/product_catalog.html'

    def get(self, request, *args, **kwargs):
        categories = selectors.get_all_categories()
        categories_with_products = [cat for cat in categories if cat.products.all()]
        
        context = {
            'categories': categories_with_products,
        }
        return render(request, self.template_name, context)




class CategoryListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = Category
    template_name = 'staff/products/category_list.html'
    context_object_name = 'categories'
    permission_required = 'products.view_category'
    paginate_by = 10
    header_title = "Gestión de Categorías"
    header_subtitle = "Organización Maestra del Menú"
    header_cta_label = "Añadir Categoría"
    header_cta_url = reverse_lazy('products:category_create')
    count_label = "Total Categorías"

    def get_queryset(self):
        return selectors.get_all_categories()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm()
        return context

class CategoryCreateView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'products.add_category'

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
        else:
            messages.error(request, 'Error al crear la categoría.')
        return redirect('products:category_list')


class CategoryUpdateView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'products.change_category'

    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoría "{category.name}" actualizada.')
        else:
            messages.error(request, 'Error al actualizar la categoría.')
        return redirect('products:category_list')


class CategoryDeleteView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'products.delete_category'

    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        name = category.name
        category.delete()
        messages.success(request, f'Categoría "{name}" eliminada.')
        return redirect('products:category_list')



class ProductListView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffListingMixin, StaffPaginationMixin, ListView):
    model = Product
    template_name = 'staff/products/product_list.html'
    context_object_name = 'products'
    permission_required = 'products.view_product'
    paginate_by = 10
    header_title = "Gestión de Inventario"
    header_subtitle = "Control Maestro de Productos y Combos"
    header_cta_label = "Nuevo Producto"
    header_cta_url = reverse_lazy('products:product_create')
    count_label = "Total Productos"

    def get_queryset(self):
        return selectors.get_all_products()


class ProductCreateView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, View):
    permission_required = 'products.add_product'
    template_name = 'staff/products/product_form.html'
    header_title = "Nuevo Producto"
    header_subtitle = "Configuración de Item en Catálogo"
    header_show_back = True
    header_back_url = reverse_lazy('products:product_list')

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        formset = ComboDetailFormSet(prefix='combo_details')
        context = self.get_context_data()
        context.update({'form': form, 'formset': formset})
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        formset = ComboDetailFormSet(request.POST, request.FILES, prefix='combo_details')

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                product = form.save()
                if product.is_combo:
                    formset.instance = product
                    formset.save()
            messages.success(request, f'Producto "{product.name}" creado correctamente.')
            return redirect('products:product_list')

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
        })


class ProductUpdateView(LoginRequiredMixin, StaffPermissionRequiredMixin, StaffHeaderMixin, View):
    permission_required = 'products.change_product'
    template_name = 'staff/products/product_form.html'
    header_title = "Editar Producto"
    header_subtitle = "Actualización de Configuración Maestra"
    header_show_back = True
    header_back_url = reverse_lazy('products:product_list')

    def get(self, request, pk, *args, **kwargs):
        product = selectors.get_product_by_id(pk)
        form = ProductForm(instance=product)
        formset = ComboDetailFormSet(instance=product, prefix='combo_details')
        context = self.get_context_data()
        context.update({
            'form': form,
            'formset': formset,
            'product': product,
        })
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ComboDetailFormSet(request.POST, request.FILES, instance=product, prefix='combo_details')

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                product = form.save()
                if product.is_combo:
                    formset.save()
                else:
                    product.combo_details.all().delete()
            messages.success(request, f'Producto "{product.name}" actualizado correctamente.')
            return redirect('products:product_list')

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'product': product,
        })


class ProductDeleteView(LoginRequiredMixin, StaffPermissionRequiredMixin, View):
    permission_required = 'products.delete_product'

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        name = product.name
        product.delete()
        messages.success(request, f'Producto "{name}" eliminado.')
        return redirect('products:product_list')