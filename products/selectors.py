from django.db.models import QuerySet
from .models import Product, Category

def get_all_products() -> QuerySet[Product]:
    """Fetch all products with their categories pre-fetched for list display."""
    return Product.objects.select_related('category').all().order_by('name')

def get_all_categories() -> QuerySet[Category]:
    """Fetch all categories with product counts."""
    return Category.objects.all().prefetch_related('products').order_by('name')

def get_product_by_id(product_id: int) -> Product:
    return Product.objects.get(id=product_id)
