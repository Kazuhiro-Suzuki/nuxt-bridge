from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from utils.exceptions import ErrorMessage as ErrMsg
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
        type='general',
        is_active=1,
    )


class TestUserView(TestCase):
    def setUp(self):
        set_up_test_data()
        self.client = APIClient()
        self.url = '/api/v1/account/user/'
        self.content_type = 'application/json'

    def test_200_ok(self):
        token, _, _ = account_repository.login(
            city_code='131032',
            email='unittest@mail.com',
            password='Passw0rd',
        )
        bearer_token = f"Bearer {token}"
        request = self.client.get(
            self.url,
            content_type=self.content_type,
            HTTP_AUTHORIZATION=bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_401_no_authorizarion(self):
        request = self.client.get(
            self.url,
            content_type=self.content_type,
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request.data['detail'], ErrMsg.INVALID_AUTH_INFO)

    def test_401_token_decode_error(self):
        token = 'tokendecodeerror'
        bearer_token = f"Bearer {token}"
        request = self.client.get(
            self.url,
            content_type=self.content_type,
            HTTP_AUTHORIZATION=bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request.data['detail'], ErrMsg.INVALID_AUTH_INFO)

    def test_401_token_expired(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVuaXR0ZXN0QG1haWwuY29tIiwiY2l0eV9jb2RlIjoiMTMxM' \
            'DMyIiwidHlwZSI6ImdlbmVyYWwiLCJleHAiOjE2MzMzMjAwOTd9.v-d4b-MUkYooWr2eOPIq-gmrp7Hrx9PPrAlrIFBAKqo'
        print(token)
        bearer_token = f"Bearer {token}"
        request = self.client.get(
            self.url,
            content_type=self.content_type,
            HTTP_AUTHORIZATION=bearer_token,
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request.data['detail'], ErrMsg.INVALID_AUTH_INFO)
