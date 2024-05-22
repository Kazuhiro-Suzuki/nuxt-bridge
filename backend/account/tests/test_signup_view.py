import json

from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from account.models import User
from app.models import Region
from utils.exceptions import ValidationException


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


class TestSignUpView(TestCase):
    def setUp(self) -> None:
        set_up_test_data()
        self.client = APIClient()
        self.url = '/api/v1/account/sign-up/'
        self.content_type = 'application/json'
        return super().setUp()

    def test_signup_200_OK(self):
        payload = {
            'email': 'unittest1@mail.com',
            'password': 'Passw0rd!',
            'password_reconfirm': 'Passw0rd!',
            'phone_number': '08012345678',
            'fax_number': '0323456789',
            'type': 'general',
            'city_code': '131032',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_500_serializer_error(self):
        payload = {
            'email': 'unittest1@mail.com',
            'password': 'Passw0rd!',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(request.data['detail'], ValidationException.default_detail)

    def test_500_no_region_error(self):
        payload = {
            'email': 'unittest2@mail.com',
            'password': 'Passw0rd!',
            'password_reconfirm': 'Passw0rd!',
            'phone_number': '08012345678',
            'fax_number': '0323456789',
            'type': 'general',
            'city_code': '131031',
        }
        request = self.client.post(self.url, data=json.dumps(payload), content_type=self.content_type)
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
