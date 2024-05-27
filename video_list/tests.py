from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser
from .models import List

class ListViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.list_data = {'list': 'Test List', 'creator': self.user.id}
        self.url = reverse('list-list')
    
    def test_create_list(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, self.list_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ListDetailsViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.list = List.objects.create(list='Test List', creator=self.user)
        self.url = reverse('list-detail', args=[self.list.pk])
    
    def test_get_list_by_user_id(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('list-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['list'], 'Test List')