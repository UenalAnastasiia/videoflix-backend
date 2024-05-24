from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserSerializer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import uuid

class RegisterViewTests(APITestCase):
    
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'password_repeat': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'image': 'path/to/image.jpg'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')


class ConfirmEmailViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            email_confirmation_token=str(uuid.uuid4()),
            is_active=False
        )
    
    def test_confirm_email(self):
        token = urlsafe_base64_encode(force_bytes(self.user.email_confirmation_token))
        url = reverse('confirm-email', args=[token])
        response = self.client.get(url)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(self.user.is_active)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='password', email_confirmed=True)
        self.login_url = reverse('login')
    
    def test_login_successful(self):
        data = {'username': 'testuser', 'password': 'password'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)
        self.assertTrue('email' in response.data)
        self.assertTrue('first_name' in response.data)
        self.assertTrue('last_name' in response.data)
        self.assertTrue('username' in response.data)
        self.assertTrue('date_joined' in response.data)
        self.assertTrue('image' in response.data)
    
    def test_login_unconfirmed_email(self):
        self.user.email_confirmed = False
        self.user.save()
        data = {'username': 'testuser', 'password': 'password'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'Bitte bestätigen Sie Ihre E-Mail, um sich einzuloggen.')


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
    
    def test_logout_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UsersViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpass123')
    
    def test_get_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class UserDetailsViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123')
    
    def test_get_user_by_pk(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        serializer = UserSerializer(CustomUser.objects.filter(id=self.user.id), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_patch_user(self):
        url = reverse('user-detail', args=[self.user.id])
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data, format='json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, 'Updated')
