from django.test import TestCase
from .models import User, Address

class AccountsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            document_number="123456789",
            phone="1234567890"
        )
        self.address = Address.objects.create(
            user=self.user,
            street="Calle 123",
            neighborhood="Los Álamos",
            city="Cali",
            reference="Cerca al parque"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.username, "test@example.com")
        self.assertTrue(self.user.check_password("password123"))

    def test_address_creation(self):
        expected_str = "Calle 123, Los Álamos, Cali"
        self.assertEqual(str(self.address), expected_str)
        self.assertEqual(self.address.user, self.user)

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            document_number="987654321"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)