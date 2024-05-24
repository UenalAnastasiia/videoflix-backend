from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Video

class VideoViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_videos(self):
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_video(self):
        url = reverse('video-list')
        data = {'title': 'Test Video', 'creator': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VideoDetailsViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.video = Video.objects.create(title='Test Video')

    def test_get_video_by_id(self):
        url = reverse('video-detail', kwargs={'pk': self.video.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_video(self):
        url = reverse('video-detail', kwargs={'pk': self.video.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_video(self):
        url = reverse('video-detail', kwargs={'pk': self.video.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserUploadsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_user_uploads(self):
        url = reverse('user-uploads', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
