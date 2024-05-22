from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from account.repositories import account_repository
from account.models import User
from app.models import Region


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


class TestUserListView(TestCase):
    def setUp(self) -> None:
        self.user = set_up_test_data()
        self.client = APIClient()
        self.url = '/api/v1/account/user-list/'
        self.content_type = 'application/json'
        token, _, _ = account_repository.login(
            email='unittest@mail.com',
            password='Passw0rd',
            city_code=131032,
        )
        self.bearer_token = f'Bearer {token}'
        return super().setUp()

    def test_200_get_ok(self):
        request = self.client.get(
            self.url + '?city_code=131032',
            HTTP_AUTHORIZATION=self.bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data[0]['email'], 'unittest@mail.com')

    def test_200_put_ok(self):
        request = self.client.put(
            self.url + f'{self.user.uid}/',
            HTTP_AUTHORIZATION=self.bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_500_get_no_param(self):
        request = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=self.bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_invalid_city_code(self):
        request = self.client.get(
            self.url + '?city_code=131031',
            HTTP_AUTHORIZATION=self.bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
