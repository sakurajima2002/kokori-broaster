from django.db.models import QuerySet
from .models import Product, Category

def get_all_products() -> QuerySet[Product]:
    return Product.objects.select_related('category').all().order_by('name')

def get_all_categories() -> QuerySet[Category]:
    return Category.objects.all().prefetch_related(
        'products__combo_details__product_child'
    ).order_by('name')


def get_product_by_id(product_id: int) -> Product:
    return Product.objects.get(id=product_id)