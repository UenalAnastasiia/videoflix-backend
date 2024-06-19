from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.category_data = {'name': 'Test Category'}
        self.url = reverse('category-list')

    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        response = self.client.post(self.url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Test Category')


class CategoryDetailsViewSetTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.url = reverse('category-detail', args=[self.category.pk])

    def test_get_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        new_data = {'name': 'Updated Category Name'}
        response = self.client.patch(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_category(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class UserCategoriesTests(APITestCase):
    def setUp(self):
        self.user_id = 1
        self.url = reverse('user-categories', args=[self.user_id])

    def test_get_user_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
