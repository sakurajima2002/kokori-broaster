from django.db import models
from accounts.models import User, Address
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('awaiting_confirmation', 'Por confirmar'),
        ('confirmed', 'Confirmado'),
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('preparing', 'En preparación'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    DELIVERY_METHOD_CHOICES = [
        ('delivery', 'Domicilio'),
        ('pickup', 'Recoger'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='awaiting_confirmation', verbose_name="Status")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, verbose_name="Delivery Method")
    stock_reduced = models.BooleanField(default=False, verbose_name="Stock Reduced")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def get_whatsapp_url(self):
        from base.models import SiteParameter
        import urllib.parse
        
        phone_param = SiteParameter.objects.filter(key='CONTACT_PHONE').first()
        phone = phone_param.value if phone_param else '573000000000'
        phone = ''.join(filter(str.isdigit, phone))
        
        message = f"🍔 *NUEVO PEDIDO - KOKORI BROASTER*\n"
        message += f"----------------------------------\n"
        message += f"🆔 *Orden*: #{self.id}\n"
        message += f"👤 *Cliente*: {self.user.get_full_name() or self.user.username}\n"
        message += f"📍 *Dirección*: {self.address.street}, {self.address.neighborhood}\n"
        message += f"----------------------------------\n"
        message += f"🛒 *Productos*:\n"
        for detail in self.details.all():
            message += f"- {detail.product.name} x{detail.quantity} (${detail.subtotal})\n"
        message += f"----------------------------------\n"
        message += f"💰 *TOTAL A PAGAR*: ${self.total}\n\n"
        message += f"✅ Por favor, confírmame el pedido para iniciar la preparación."
        
        return f"https://api.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}"

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