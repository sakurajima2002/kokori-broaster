from django.db.models import QuerySet
from .models import Order, Delivery, Rating

def get_all_orders() -> QuerySet[Order]:
    
    return Order.objects.select_related('user', 'address').all().order_by('-order_date')

def get_order_by_id(order_id: int) -> Order:
    
    return Order.objects.select_related('user', 'address', 'payment', 'delivery')\
                        .prefetch_related('details__product')\
                        .get(id=order_id)

def get_all_deliveries() -> QuerySet[Delivery]:
    
    return Delivery.objects.select_related('order__user').all().order_by('-departure_date')

def get_all_ratings() -> QuerySet[Rating]:
    
    return Rating.objects.select_related('user', 'order').all().order_by('-rating_date')