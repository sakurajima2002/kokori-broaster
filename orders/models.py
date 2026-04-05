from django.db import models
from accounts.models import User, Address
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    DELIVERY_METHOD_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, verbose_name="Delivery Method")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')
    quantity = models.IntegerField(verbose_name="Quantity")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('transfer', 'Transfer'),
        ('cash', 'Cash'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Payment Method")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Status")
    transaction_ref = models.CharField(max_length=100, blank=True, verbose_name="Transaction Reference")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Payment Date")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment for Order {self.order.id}"

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    departure_date = models.DateTimeField(verbose_name="Departure Date")
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name="Delivery Date")
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Tracking Number")

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

    def __str__(self):
        return f"Delivery for Order {self.order.id}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='rating')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Score")
    comment = models.TextField(blank=True, verbose_name="Comment")
    rating_date = models.DateField(auto_now_add=True, verbose_name="Rating Date")

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = ('user', 'order')

    def __str__(self):
        return f"Rating {self.score} for Order {self.order.id}"
