import json

from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from account.models import User
from app.models import Region
from utils.exceptions import ErrorMessage as ErrMsg


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


class TestTokenObtainView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = '/api/v1/account/token-obtain/'
        self.content_type = 'application/json'
        self.user = set_up_test_data()
        return super().setUp()

    def test_200_ok(self):
        # 正常：通常ログイン
        payload = {
            'email': 'unittest@mail.com',
            'password': 'Passw0rd',
            'city_code': '131032',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_401_password_incorrect(self):
        # エラー：パスワード間違い
        payload = {
            'email': 'unittest@mail.com',
            'password': 'Password1',
            'city_code': '131032',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request.data['detail'], ErrMsg.INCORRECT_PASSWORD)

    def test_401_no_user(self):
        # エラー：メールアドレスのユーザいない
        payload = {
            'email': 'unittest1@mail.com',
            'password': 'Passw0rd',
            'city_code': '131032',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request.data['detail'], ErrMsg.NO_USER)

    def test_200_from_app(self):
        # 正常：アプリのミライロ画面からログイン
        payload = {
            'email': 'unittest@mail.com',
            'city_code': '131032',
            'from_path': 'mirairo',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertIn('token', request.data)
        self.assertIn('refresh_token', request.data)
        self.assertIn('type', request.data)

    def test_401_from_app_no_user(self):
        # メールアドレスのユーザいない
        payload = {
            'email': 'unittesttest@mail.com',
            'city_code': '131032',
            'from_path': 'mirairo',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request.data['detail'], ErrMsg.NO_USER)

    def test_401_not_from_app(self):
        # アプリからのアクセスでない
        payload = {
            'email': 'unittest@mail.com',
            'city_code': '131032',
            'from_path': 'not_from_app',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(request.data['detail'], ErrMsg.NOT_FROM_APP)

    def test_500_serializer_error(self):
        payload = {
            'email': 'unittest@mail.com',
            'password': 'Passw0rd',
            # 'city_code': '131032',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
