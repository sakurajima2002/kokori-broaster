from django.test import TestCase
from accounts.models import User, Address
from products.models import Product, Category
from .models import Order, OrderDetail, Payment, Delivery, Rating
from decimal import Decimal
from django.utils import timezone

class OrdersModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.user = User.objects.create_user(email="buyer@example.com", document_number="111")
        self.address = Address.objects.create(user=self.user, street="St 1", neighborhood="N1", city="C1")
        self.product = Product.objects.create(category=self.category, name="Burger", price=Decimal("15.00"), stock=100)
        
        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            total=Decimal("15.00"),
            delivery_method='delivery'
        )
        self.order_detail = OrderDetail.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("15.00"),
            subtotal=Decimal("15.00")
        )

    def test_order_creation(self):
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(str(self.order), f"Order {self.order.id} - buyer@example.com")

    def test_order_detail_creation(self):
        self.assertEqual(str(self.order_detail), "Burger x1")

    def test_payment_creation(self):
        payment = Payment.objects.create(
            order=self.order,
            payment_method='cash',
            status='completed'
        )
        self.assertEqual(str(payment), f"Payment for Order {self.order.id}")

    def test_delivery_creation(self):
        delivery = Delivery.objects.create(
            order=self.order,
            departure_date=timezone.now()
        )
        self.assertEqual(str(delivery), f"Delivery for Order {self.order.id}")

    def test_rating_creation(self):
        rating = Rating.objects.create(
            user=self.user,
            order=self.order,
            score=5,
            comment="Great!"
        )
        self.assertEqual(str(rating), f"Rating 5 for Order {self.order.id}")