from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.models import User, Address, Municipality
from products.models import Product, Category
from orders.models import Order, OrderDetail, Delivery, Rating
from orders.cart import Cart
from orders import services
from decimal import Decimal
from django.utils import timezone

class OrdersModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.user = User.objects.create_user(email="buyer@example.com", password="password123", document_number="111")
        self.municipality = Municipality.objects.create(name="Cali", code="76001")
        self.address = Address.objects.create(user=self.user, street="St 1", neighborhood="N1", municipality=self.municipality)
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
        self.assertEqual(self.order.status, 'awaiting_confirmation')
        self.assertEqual(str(self.order), f"Order {self.order.id} - buyer@example.com")

    def test_order_detail_creation(self):
        self.assertEqual(str(self.order_detail), "Burger x1")


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


class CartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(self.request)
        self.request.session.save()
        
        self.category = Category.objects.create(name="Food")
        self.product1 = Product.objects.create(category=self.category, name="Burger", price=Decimal("10.00"), stock=10)
        self.product2 = Product.objects.create(category=self.category, name="Fries", price=Decimal("5.00"), stock=20)
        self.cart = Cart(self.request)

    def test_add_product(self):
        self.cart.add(self.product1, quantity=2)
        self.assertEqual(len(self.cart), 2)
        self.assertEqual(self.cart.get_total_price(), Decimal("20.00"))

    def test_add_product_override(self):
        self.cart.add(self.product1, quantity=2)
        self.cart.add(self.product1, quantity=3, override_quantity=True)
        self.assertEqual(len(self.cart), 3)

    def test_remove_product(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.remove(self.product1)
        self.assertEqual(len(self.cart), 0)

    def test_clear_cart(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.clear()
        self.assertEqual(len(self.cart), 0)

    def test_iter_cart(self):
        self.cart.add(self.product1, quantity=1)
        self.cart.add(self.product2, quantity=2)
        items = list(self.cart)
        self.assertEqual(len(items), 2)


class ServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="buyer@example.com", password="password123", document_number="111")
        self.municipality = Municipality.objects.create(name="Cali", code="76001")
        self.address = Address.objects.create(user=self.user, street="St 1", municipality=self.municipality)
        self.category = Category.objects.create(name="Food")
        self.product = Product.objects.create(category=self.category, name="Burger", price=Decimal("15.00"), stock=1)
        
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(self.request)
        self.request.session.save()
        self.cart = Cart(self.request)
        self.cart.add(self.product, quantity=1)

    def test_validate_stock_fail(self):
        self.cart.add(self.product, quantity=2, override_quantity=True)
        with self.assertRaises(ValueError):
            services.validate_stock(self.cart)

    def test_process_checkout_and_update(self):
        order = services.process_checkout(self.user, self.cart, self.address)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'awaiting_confirmation')
        self.assertEqual(Order.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1) # Stock not reduced yet
        
        # Move to confirmed to trigger stock reduction
        services.update_order_status(order, "confirmed")
        self.assertEqual(order.status, "confirmed")
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 0)
        
        services.update_order_status(order, "paid")
        services.update_order_status(order, "preparing")
        services.update_order_status(order, "shipped")
        self.assertEqual(order.status, "shipped")
        
        services.update_order_status(order, "delivered")
        self.assertEqual(order.status, "delivered")
        self.assertIsNotNone(order.delivery.delivery_date)


class OrdersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="buyer@example.com", password="password123", document_number="111")
        self.staff_user = User.objects.create_superuser(email="staff@example.com", password="password123", document_number="222")
        self.municipality = Municipality.objects.create(name="Cali", code="76001")
        self.address = Address.objects.create(user=self.user, street="St 1", municipality=self.municipality)
        self.category = Category.objects.create(name="Food")
        self.product = Product.objects.create(category=self.category, name="Burger", price=Decimal("15.00"), stock=100)
        
        self.order = Order.objects.create(
            user=self.user,
            address=self.address,
            total=Decimal("15.00"),
            delivery_method='delivery',
            status='delivered'
        )

    def test_cart_add_remove_views(self):
        response = self.client.post(reverse('orders:cart_add', args=[self.product.id]), {'quantity': 2})
        self.assertRedirects(response, reverse('products:product_catalog'))
        
        response = self.client.post(reverse('orders:cart_remove', args=[self.product.id]))
        self.assertRedirects(response, reverse('products:product_catalog'))

    def test_checkout_view_get(self):
        self.client.login(username="buyer@example.com", password="password123")
        # Empty cart
        response = self.client.get(reverse('orders:checkout'))
        self.assertRedirects(response, reverse('products:product_catalog'))
        
        # With items
        self.client.post(reverse('orders:cart_add', args=[self.product.id]), {'quantity': 1})
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_post_valid(self):
        self.client.login(username="buyer@example.com", password="password123")
        self.client.post(reverse('orders:cart_add', args=[self.product.id]), {'quantity': 1})
        
        response = self.client.post(reverse('orders:checkout'), {
            'address_id': self.address.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://api.whatsapp.com/send')
        self.assertEqual(Order.objects.count(), 2)

    def test_checkout_view_post_invalid(self):
        self.client.login(username="buyer@example.com", password="password123")
        self.client.post(reverse('orders:cart_add', args=[self.product.id]), {'quantity': 1})
        response = self.client.post(reverse('orders:checkout'), {})
        self.assertEqual(response.status_code, 200)

    def test_ratings_views(self):
        self.client.login(username="buyer@example.com", password="password123")
        # Create
        response = self.client.post(reverse('orders:rating_create', args=[self.order.id]), {
            'score': 5,
            'comment': 'Awesome!'
        })
        self.assertRedirects(response, reverse('accounts:my_orders'))
        self.assertEqual(Rating.objects.count(), 1)
        rating = Rating.objects.first()
        self.assertEqual(rating.score, 5)

        # Update
        response = self.client.post(reverse('orders:rating_update', args=[rating.id]), {
            'score': 4,
            'comment': 'Good'
        })
        self.assertRedirects(response, reverse('accounts:my_orders'))
        rating.refresh_from_db()
        self.assertEqual(rating.score, 4)
        
        # Delete
        response = self.client.post(reverse('orders:rating_delete', args=[rating.id]))
        self.assertRedirects(response, reverse('accounts:my_orders'))
        self.assertEqual(Rating.objects.count(), 0)

    def test_rating_create_not_delivered(self):
        self.client.login(username="buyer@example.com", password="password123")
        self.order.status = 'awaiting_confirmation'
        self.order.save()
        response = self.client.post(reverse('orders:rating_create', args=[self.order.id]), {
            'score': 5,
            'comment': 'Awesome!'
        })
        self.assertEqual(response.status_code, 404)

    def test_staff_views(self):
        self.client.login(username="staff@example.com", password="password123")
        
        # Prepare order for shipment
        self.order.status = 'preparing'
        self.order.save()
        
        # Delivery update
        response = self.client.post(reverse('orders:update_delivery_status', args=[self.order.id]), {'status': 'shipped'})
        self.assertRedirects(response, reverse('orders:delivery_list'))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'shipped')
        
        rating = Rating.objects.create(user=self.user, order=self.order, score=5, comment="Great!")
        response = self.client.post(reverse('orders:staff_rating_delete', args=[rating.id]))
        self.assertRedirects(response, reverse('orders:rating_list'))
        self.assertEqual(Rating.objects.count(), 0)


    def test_municipality_crud(self):
        self.client.login(username="staff@example.com", password="password123")
        
        # List
        response = self.client.get(reverse('orders:municipality_list'))
        self.assertEqual(response.status_code, 200)
        
        # Create
        response = self.client.post(reverse('orders:municipality_create'), {
            'name': 'New Mun',
            'code': '123'
        })
        self.assertRedirects(response, reverse('orders:municipality_list'))
        self.assertEqual(Municipality.objects.filter(name='New Mun').count(), 1)
        
        # Update
        m = Municipality.objects.get(name='New Mun')
        response = self.client.post(reverse('orders:municipality_update', args=[m.id]), {
            'name': 'Updated Mun',
            'code': '456'
        })
        self.assertRedirects(response, reverse('orders:municipality_list'))
        m.refresh_from_db()
        self.assertEqual(m.name, 'Updated Mun')
        
        # Delete
        response = self.client.post(reverse('orders:municipality_delete', args=[m.id]))
        self.assertRedirects(response, reverse('orders:municipality_list'))
        self.assertEqual(Municipality.objects.filter(name='Updated Mun').count(), 0)
