import json

from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from account.models import User
from app.models import Region
from account.repositories import account_repository


def set_up_test_data():
    region, _ = Region.objects.get_or_create(
        name='Minato City',
        city_code=131032,
        header_image='top4-minato.png',
        header_text='みなと障がい者支援アプリ',
        base_color='purple'
    )
    user, _ = User.objects.get_or_create(
        email='unittest@mail.com',
        password=make_password('Passw0rd'),
        region=region,
        phone_number='09012345678',
        fax_number='0312345678',
        type='business',
        is_active=1,
    )
    return user


class TestTokenRefreshView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = '/api/v1/account/token-refresh/'
        self.content_type = 'application/json'
        self.user = set_up_test_data()
        token, _, refresh_token = account_repository.login(
            city_code='131032',
            email='unittest@mail.com',
            password='Passw0rd',
        )
        self.bearer_token = 'Bearer ' + token
        self.refresh_token = refresh_token
        return super().setUp()

    def test_200_ok(self):
        payload = {
            'refresh_token': self.refresh_token,
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_500_serializer_error(self):
        payload = {
            # 'refresh_token': self.refresh_token,
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
