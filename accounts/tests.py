from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Address, Municipality

class AccountsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            document_number="123456789",
            phone="1234567890"
        )
        self.municipality = Municipality.objects.create(name="Cali", code="76001")
        self.address = Address.objects.create(
            user=self.user,
            street="Calle 123",
            neighborhood="Los Álamos",
            municipality=self.municipality,
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

class AccountsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            document_number="1111"
        )
        self.staff_user = User.objects.create_superuser(
            email="staff@example.com",
            password="password123",
            document_number="2222"
        )
        self.address = Address.objects.create(
            user=self.user,
            street="Street 1"
        )

    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user@example.com',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home'))

        # Invalid login
        response = self.client.post(reverse('accounts:login'), {
            'username': 'user@example.com',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username="user@example.com", password="password123")
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))

    def test_home_view_public(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_staff(self):
        self.client.login(username="staff@example.com", password="password123")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_users', response.context)

    def test_my_account_view(self):
        self.client.login(username="user@example.com", password="password123")
        response = self.client.get(reverse('accounts:my_account'))
        self.assertEqual(response.status_code, 200)
        
        # Test valid post
        response = self.client.post(reverse('accounts:my_account'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone': '9999999',
            'email': 'user@example.com',
            'document_number': '1111',
            'document_type': 'CC',
            'update_profile': '',
        })
        self.assertRedirects(response, reverse('accounts:my_account'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')

    def test_delete_address_view(self):
        self.client.login(username="user@example.com", password="password123")
        response = self.client.post(reverse('accounts:delete_address', args=[self.address.id]))
        self.assertRedirects(response, reverse('accounts:my_account'))
        self.assertEqual(Address.objects.count(), 0)

    def test_my_orders_view(self):
        self.client.login(username="user@example.com", password="password123")
        response = self.client.get(reverse('accounts:my_orders'))
        self.assertEqual(response.status_code, 200)

    def test_user_staff_toggle_view(self):
        self.client.login(username="staff@example.com", password="password123")
        # Ensure cannot toggle self
        response = self.client.post(reverse('accounts:user_staff_toggle', args=[self.staff_user.id]))
        self.assertRedirects(response, reverse('accounts:user_list'))
        
        # Toggle other user
        self.assertFalse(self.user.is_staff)
        response = self.client.post(reverse('accounts:user_staff_toggle', args=[self.user.id]))
        self.assertRedirects(response, reverse('accounts:user_list'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)