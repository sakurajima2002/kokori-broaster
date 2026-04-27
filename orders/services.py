from django.db import transaction
from django.utils import timezone
from .models import Order, OrderDetail, Delivery, Payment

def validate_stock(cart):
    for item in cart:
        if item['product'].stock < item['quantity']:
            raise ValueError(f"No hay stock suficiente para {item['product'].name}.")

def reduce_stock(cart):
    for item in cart:
        product = item['product']
        product.stock -= item['quantity']
        product.save()

def create_order_record(user, address, cart):
    order = Order.objects.create(
        user=user,
        address=address,
        total=cart.get_total_price(),
        status='paid',
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

def create_payment_record(order, payment_method):
    return Payment.objects.create(
        order=order,
        payment_method=payment_method,
        status='completed',
        transaction_ref=f"MOCK-{order.id}"
    )

def create_delivery_record(order):
    delivery = Delivery.objects.create(
        order=order,
        departure_date=timezone.now(),
        tracking_number=f"TRK-{order.id:05d}"
    )
    order.status = 'preparing'
    order.save()
    return delivery

def process_checkout(user, cart, address, payment_method):
    validate_stock(cart)
    
    with transaction.atomic():
        order = create_order_record(user, address, cart)
        reduce_stock(cart)
        create_payment_record(order, payment_method)
        create_delivery_record(order)
        
    return order
def update_order_status(order, new_status):
    order.status = new_status
    order.save()
    
    if new_status == 'delivered':
        delivery = getattr(order, 'delivery', None)
        if delivery:
            delivery.delivery_date = timezone.now()
            delivery.save()
    return order
