from django import forms
from .models import Product, ComboDetail, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock', 'image', 'is_combo']
        widgets = {
            'image': forms.FileInput(),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


ComboDetailFormSet = forms.inlineformset_factory(
    Product, ComboDetail,
    fk_name='combo_parent',
    fields=['product_child', 'quantity'],
    extra=1,
    can_delete=True
)
