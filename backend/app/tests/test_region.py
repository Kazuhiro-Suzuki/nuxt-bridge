from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from app.models import Region


class RegionViewTest(TestCase):
    def setUp(self):
        Region.objects.create(
            name='Minato City',
            city_code='131032',
            email='lg.pwd.minato@gmail.com',
            header_text='みなと障害者支援アプリ',
            header_image='image-minato.png',
            top_image='top4-minato.jpg',
            base_color='purple',
        )
        self.url = '/api/v1/app/region/'
        self.client = APIClient()

    def test_500_get_no_city_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_invalid_city_code(self):
        response = self.client.get(self.url, {'city_code': '111111'})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_200_get_ok(self):
        response = self.client.get(self.url, {'city_code': '131032'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {
            "id": 1,
            "created_by": None,
            "updated_by": None,
            "name": "Minato City",
            "city_code": "131032",
            "active_since": None,
            "active_until": None,
            "email": "lg.pwd.minato@gmail.com",
            "header_image": "image-minato.png",
            "top_image": "top4-minato.jpg",
            "header_text": "みなと障害者支援アプリ",
            "base_color": "purple"
        })
