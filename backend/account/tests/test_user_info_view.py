import json

from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from account.repositories import account_repository
from account.models import User, UserCityCa
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
        type='general',
        is_active=1,
    )
    user2, _ = User.objects.get_or_create(
        email='unittest2@mail.com',
        password=make_password('Passw0rd'),
        region=region,
        phone_number='09012345679',
        fax_number='0312345679',
        type='business',
        is_active=1,
    )
    user_ca = UserCityCa.objects.create(
        user=user,
        uid='uid',
    )
    return user, user_ca, user2


class TestUserInfoView(TestCase):
    def setUp(self) -> None:
        self.user, self.user_ca, self.user2 = set_up_test_data()
        self.client = APIClient()
        self.url = '/api/v1/account/user-info/'
        self.content_type = 'application/json'
        token, _, _ = account_repository.login(
            email='unittest@mail.com',
            password='Passw0rd',
            city_code=131032,
        )
        self.bearer_token = f'Bearer {token}'
        token2, _, _ = account_repository.login(
            email='unittest2@mail.com',
            password='Passw0rd',
            city_code=131032,
        )
        self.bearer_token = f'Bearer {token}'
        self.bearer_token2 = f'Bearer {token2}'
        return super().setUp()

    def test_200_ok_get_general_user(self):
        request = self.client.get(
            self.url,
            content_type=self.content_type,
            HTTP_AUTHORIZATION=self.bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_200_ok_get_business_user(self):
        request = self.client.get(
            self.url,
            content_type=self.content_type,
            HTTP_AUTHORIZATION=self.bearer_token2,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_200_put_ok(self):
        payload = {
            'email': 'unittest2@mail.com',
            'phone_number': '08011112222',
            'fax_number': '0312345671',
        }
        request = self.client.put(
            self.url + str(self.user2.uid) + '/',
            data=json.dumps(payload),
            content_type=self.content_type,
            HTTP_AUTHORIZATION=self.bearer_token2,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        user2 = User.objects.get(uid=str(self.user2.uid))
        self.assertEqual(user2.phone_number, '08011112222')
        self.assertEqual(user2.fax_number, '0312345671')

    def test_500_put_serializer_error(self):
        payload = {
            'email': 'unittest2@mail.com',
            # 'phone_number': '08011112222',
            'fax_number': '0312345671',
        }
        request = self.client.put(
            self.url + str(self.user2.uid) + '/',
            data=json.dumps(payload),
            content_type=self.content_type,
            HTTP_AUTHORIZATION=self.bearer_token2,
        )
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
