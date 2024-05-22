from django.test import TestCase
from rest_framework import status


class CommonViewTest(TestCase):
    def test_health_check(self):
        response = self.client.get('/api/health-check/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
