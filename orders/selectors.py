from django.db.models import QuerySet
from .models import Order, Delivery, Rating

def get_all_orders() -> QuerySet[Order]:
    """Fetch all orders with user and address details."""
    return Order.objects.select_related('user', 'address').all().order_by('-order_date')

def get_order_by_id(order_id: int) -> Order:
    """Fetch a single order with full details and related fields."""
    return Order.objects.select_related('user', 'address', 'payment', 'delivery')\
                        .prefetch_related('details__product')\
                        .get(id=order_id)

def get_all_deliveries() -> QuerySet[Delivery]:
    """Fetch all deliveries with associated orders and users."""
    return Delivery.objects.select_related('order__user').all().order_by('-departure_date')

def get_all_ratings() -> QuerySet[Rating]:
    """Fetch all ratings with user and order context."""
    return Rating.objects.select_related('user', 'order').all().order_by('-rating_date')
