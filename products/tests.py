from django.test import TestCase
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
        self.assertEqual(self.category._meta.verbose_name, "Category")

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