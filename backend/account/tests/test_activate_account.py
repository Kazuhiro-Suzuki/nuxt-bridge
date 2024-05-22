import json

from django.test import TestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient

from utils.exceptions import ErrorMessage as ErrMsg
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
        is_active=0,
    )
    user2, _ = User.objects.get_or_create(
        email='unittest2@mail.com',
        password=make_password('Passw0rd'),
        region=region,
        phone_number='09012345679',
        fax_number='0312345679',
        type='general',
        is_active=1,
    )
    return user, user2


class TestActivateAccount(TestCase):
    def setUp(self) -> None:
        self.user, self.user2 = set_up_test_data()
        self.client = APIClient()
        self.url = '/api/v1/account/activate/'
        self.content_type = 'application/json'
        return super().setUp()

    def test_200_ok(self):
        payload = {
            'uid': str(self.user.uid),
            'city_code': 131032,
        }
        request = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type=self.content_type,
        )
        updated_user = User.objects.get(uid=str(self.user.uid))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertTrue(updated_user.is_active)

    def test_500_serializer_error(self):
        payload = {
            'uid': str(self.user.uid),
            # 'city_code': 131032,
        }
        request = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type=self.content_type,
        )
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_already_active(self):
        payload = {
            'uid': str(self.user2.uid),
            'city_code': 131032,
        }
        request = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type=self.content_type,
        )
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(request.data['detail'], ErrMsg.ALREADY_VALID_ACCOUNT)
