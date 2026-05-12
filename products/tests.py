from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from .models import Category, Product, ComboDetail
from decimal import Decimal

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name="Basic Product 1",
            price=Decimal("10.00"),
            stock=10
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Basic Product 2",
            price=Decimal("15.00"),
            stock=5
        )
        self.combo = Product.objects.create(
            category=self.category,
            name="Mega Combo",
            price=Decimal("20.00"),
            is_combo=True,
            stock=10
        )
        ComboDetail.objects.create(combo_parent=self.combo, product_child=self.product1, quantity=1)
        ComboDetail.objects.create(combo_parent=self.combo, product_child=self.product2, quantity=1)

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_product_creation(self):
        self.assertEqual(str(self.product1), "Basic Product 1")
        self.assertEqual(self.product1.price, Decimal("10.00"))

    def test_combo_properties(self):
        self.assertEqual(self.combo.original_value, Decimal("25.00"))
        self.assertEqual(self.combo.savings, Decimal("5.00"))

    def test_non_combo_properties(self):
        self.assertEqual(self.product1.original_value, Decimal("10.00"))
        self.assertEqual(self.product1.savings, Decimal("0"))

    def test_combo_detail_creation(self):
        detail = ComboDetail.objects.get(combo_parent=self.combo, product_child=self.product1)
        self.assertEqual(str(detail), f"{self.combo.name} - {self.product1.name} x1")


class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(email="staff@example.com", password="password123", document_number="222")
        self.category = Category.objects.create(name="Food")
        self.product = Product.objects.create(category=self.category, name="Burger", price=Decimal("10.00"), stock=10)

    def test_product_catalog_view(self):
        response = self.client.get(reverse('products:product_catalog'))
        self.assertEqual(response.status_code, 200)

    def test_category_views(self):
        self.client.login(username="staff@example.com", password="password123")
        # List
        response = self.client.get(reverse('products:category_list'))
        self.assertEqual(response.status_code, 200)
        # Create
        response = self.client.post(reverse('products:category_create'), {'name': 'Drinks', 'description': 'desc'})
        self.assertRedirects(response, reverse('products:category_list'))
        # Create Invalid
        response = self.client.post(reverse('products:category_create'), {'name': ''})
        self.assertRedirects(response, reverse('products:category_list'))
        # Update
        response = self.client.post(reverse('products:category_update', args=[self.category.id]), {'name': 'Updated Food'})
        self.assertRedirects(response, reverse('products:category_list'))

    def test_product_staff_views(self):
        self.client.login(username="staff@example.com", password="password123")
        # GET
        response = self.client.get(reverse('products:product_create'))
        self.assertEqual(response.status_code, 200)
        # List
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        # Create (Basic)
        response = self.client.post(reverse('products:product_create'), {
            'category': self.category.id,
            'name': 'Soda',
            'price': '2.00',
            'stock': '50',
            'combo_details-TOTAL_FORMS': '0',
            'combo_details-INITIAL_FORMS': '0',
            'combo_details-MIN_NUM_FORMS': '0',
            'combo_details-MAX_NUM_FORMS': '1000',
        })
        self.assertRedirects(response, reverse('products:product_list'))
        
        # Update
        response = self.client.post(reverse('products:product_update', args=[self.product.id]), {
            'category': self.category.id,
            'name': 'Updated Burger',
            'price': '12.00',
            'stock': '8',
            'combo_details-TOTAL_FORMS': '0',
            'combo_details-INITIAL_FORMS': '0',
            'combo_details-MIN_NUM_FORMS': '0',
            'combo_details-MAX_NUM_FORMS': '1000',
        })
        self.assertRedirects(response, reverse('products:product_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Burger')

        # Delete
        response = self.client.post(reverse('products:product_delete', args=[self.product.id]))
        self.assertRedirects(response, reverse('products:product_list'))

    def test_category_delete_view(self):
        self.client.login(username="staff@example.com", password="password123")
        response = self.client.post(reverse('products:category_delete', args=[self.category.id]))
        self.assertRedirects(response, reverse('products:category_list'))
        self.assertEqual(Category.objects.count(), 0)