import json
import datetime

from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from account.models import User, ResetPassword
from app.models import Region
from account.repositories import account_repository
from config import settings


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
    ResetPassword.objects.create(
        user=user,
        expiration_at=datetime.datetime.now() + settings.RESET_PASSWORD_TIME
    )
    return user


class TestResetPasswordView(TestCase):
    def setUp(self) -> None:
        self.user = set_up_test_data()
        self.client = APIClient()
        self.request_url = '/api/v1/account/request-reset-password/'
        self.reset_url = '/api/v1/account/reset-password/'
        self.content_type = 'application/json'
        token, _, _ = account_repository.login(
            email='unittest@mail.com',
            password='Passw0rd',
            city_code=131032,
        )
        self.bearer_token = f'Bearer {token}'
        return super().setUp()

    '''
    パスワード変更リクエスト
    '''

    def test_200_request_ok(self):
        payload = {
            'email': 'unittest@mail.com',
            'city_code': '131032',
        }
        request = self.client.post(
            self.request_url,
            data=json.dumps(payload),
            content_type=self.content_type,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_400_request_serializer_error(self):
        payload = {
            'email': 'unittest@mail.com',
            # 'city_code': '131032',
        }
        request = self.client.post(
            self.request_url,
            data=json.dumps(payload),
            content_type=self.content_type,
        )
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    '''
    パスワード変更実行
    '''

    def test_200_reset_ok(self):
        reset_password_obj = ResetPassword.objects.first()
        payload = {
            'password': 'updatedPassw0rd',
            'password_reconfirm': 'updatedPassw0rd',
            'uid': str(reset_password_obj.uid),
        }
        request = self.client.post(
            self.reset_url,
            data=json.dumps(payload),
            content_type=self.content_type,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_500_request_serializer_error(self):
        payload = {
            'password': 'updatedPassw0rd',
            'password_reconfirm': 'updatedPassw0rd',
            # 'uid': 'uid',
        }
        request = self.client.post(
            self.reset_url,
            data=json.dumps(payload),
            content_type=self.content_type,
        )
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
