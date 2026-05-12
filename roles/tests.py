from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from accounts.models import User

class RolesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(email="admin@example.com", password="password123", document_number="111")
        self.group = Group.objects.create(name="Managers")

    def test_roles_views_as_admin(self):
        self.client.login(username="admin@example.com", password="password123")
        
        # List
        response = self.client.get(reverse('roles:group_list'))
        self.assertEqual(response.status_code, 200)
        
        # Create
        response = self.client.post(reverse('roles:group_create'), {'name': 'New Role'})
        self.assertRedirects(response, reverse('roles:group_list'))
        
        # Update
        response = self.client.post(reverse('roles:group_edit', args=[self.group.id]), {'name': 'Updated Role'})
        self.assertRedirects(response, reverse('roles:group_list'))
        
        # Delete
        response = self.client.post(reverse('roles:group_delete', args=[self.group.id]))
        self.assertRedirects(response, reverse('roles:group_list'))

    def test_user_role_update_view(self):
        self.client.login(username="admin@example.com", password="password123")
        other_user = User.objects.create_user(email="other@example.com", password="password123", document_number="333")
        
        response = self.client.get(reverse('roles:user_role_edit', args=[other_user.id]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('roles:user_role_edit', args=[other_user.id]), {
            'groups': [self.group.id]
        })
        self.assertRedirects(response, reverse('accounts:user_list'))

    def test_unauthorized_access(self):
        _unused_regular_user = User.objects.create_user(email="reg@example.com", password="password123", document_number="444")
        self.client.login(username="reg@example.com", password="password123")
        
        response = self.client.get(reverse('roles:group_list'))
        # The mixin returns 403 for unauthorized staff access
        self.assertEqual(response.status_code, 403)
