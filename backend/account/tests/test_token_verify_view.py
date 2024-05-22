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


class TestTokenVerifyView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = '/api/v1/account/token-verify/'
        self.content_type = 'application/json'
        self.user = set_up_test_data()
        token, _, _ = account_repository.login(
            city_code='131032',
            email='unittest@mail.com',
            password='Passw0rd',
        )
        self.bearer_token = 'Bearer ' + token
        return super().setUp()

    def test_200_ok(self):
        request = self.client.post(
            self.url,
            content_type=self.content_type,
            HTTP_AUTHORIZATION=self.bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_401_no_authorization_error(self):
        request = self.client.post(
            self.url,
            content_type=self.content_type,
            # HTTP_AUTHORIZATION=self.bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
