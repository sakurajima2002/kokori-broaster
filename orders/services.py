from django.db import transaction
from django.utils import timezone
from .models import Order, OrderDetail, Delivery

def validate_stock(cart):
    for item in cart:
        if item['product'].stock < item['quantity']:
            raise ValueError(f"No hay stock suficiente para {item['product'].name}.")

def reduce_order_stock(order):
    if order.stock_reduced:
        return
    for detail in order.details.all():
        product = detail.product
        product.stock -= detail.quantity
        product.save()
    order.stock_reduced = True
    order.save()

def create_order_record(user, address, cart):
    order = Order.objects.create(
        user=user,
        address=address,
        total=cart.get_total_price(),
        status='awaiting_confirmation',
        delivery_method='delivery'
    )
    
    for item in cart:
        OrderDetail.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            unit_price=item['price'],
            subtotal=item['total_price']
        )
    return order


def create_delivery_record(order):
    delivery = Delivery.objects.create(
        order=order,
        departure_date=timezone.now(),
        tracking_number=f"TRK-{order.id:05d}"
    )
    return delivery

def process_checkout(user, cart, address):
    validate_stock(cart)
    
    with transaction.atomic():
        order = create_order_record(user, address, cart)
        # We no longer reduce stock here. It happens on confirmation.
        create_delivery_record(order)
        
    return order

def validate_status_transition(current_status, new_status):
    """
    Ensures orders follow a strict sequence:
    awaiting_confirmation -> confirmed -> paid -> preparing -> shipped -> delivered
    """
    SEQUENCE = [
        'awaiting_confirmation',
        'confirmed',
        'paid',
        'preparing',
        'shipped',
        'delivered'
    ]
    
    if new_status == 'cancelled':
        return True # Can cancel anytime (business rule assumption)
        
    if current_status not in SEQUENCE or new_status not in SEQUENCE:
        return False
        
    current_idx = SEQUENCE.index(current_status)
    new_idx = SEQUENCE.index(new_status)
    
    # Allow staying in same status or moving exactly to the next one
    return new_idx == current_idx + 1 or new_idx == current_idx

def update_order_status(order, new_status):
    if not validate_status_transition(order.status, new_status):
        raise ValueError(f"No se puede pasar de {order.get_status_display()} a {dict(order.STATUS_CHOICES).get(new_status)}.")

    with transaction.atomic():
        order.status = new_status
        
        # Trigger stock reduction if confirmed
        if new_status == 'confirmed':
            reduce_order_stock(order)
            
        order.save()
        
        if new_status == 'delivered':
            delivery = getattr(order, 'delivery', None)
            if delivery:
                delivery.delivery_date = timezone.now()
                delivery.save()
    return order
