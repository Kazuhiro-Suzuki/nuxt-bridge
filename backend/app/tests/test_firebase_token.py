from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from account.repositories import account_repository
from app.models.firebase_token import FirebaseToken
from app.models.region import Region
from app.views.firebase_token_view import FirebaseTokenView, FirebaseTokenVerifyView


User = get_user_model()


def set_up_test_data():
    user = User.objects.create_user(
        email='test-user@gmail.com',
        password='test',
        phone_number='123456',
        type='general_user'
    )

    (token, _, _) = account_repository.generate_jwt(
        email=user.email,
        type=user.type,
        city_code='131032'
    )

    region = Region.objects.create(
        name='Minato City',
        city_code='131032',
        email='lg.pwd.minato@gmail.com',
        header_text='みなと障害者支援アプリ',
        header_image='image-minato.png',
        top_image='top4-minato.jpg',
        base_color='purple',
    )

    FirebaseToken.objects.create(
        token=token,
        region=region,
    )

    return user, token


class FirebaseTokenViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.url = '/api/v1/app/firebase_token/'
        self.client = APIRequestFactory()
        self.view = FirebaseTokenView.as_view()

    def test_201_post_ok(self):
        request = self.client.post(self.url, {
            "city_code": "131032",
            "token": self.token
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_500_post_no_token(self):
        request = self.client.post(self.url, {
            "city_code": "131032"
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_post_invalid_city_code(self):
        request = self.client.post(self.url, {
            "city_code": "11111",
            "token": self.token
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_200_get_ok(self):
        request = self.client.get(self.url, {
            "city_code": "131032",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_500_get_no_city_code(self):
        request = self.client.get(self.url)

        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_invalid_city_code(self):
        request = self.client.get(self.url, {
            "city_code": "11111",
        })

        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class FirebaseTokenVerifyViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.url = '/api/v1/app/firebase_verify_token/'
        self.client = APIRequestFactory()
        self.view = FirebaseTokenVerifyView.as_view()

    def test_200_post_ok(self):
        request = self.client.post(self.url, {
            "token": self.token,
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_500_post_no_token(self):
        request = self.client.post(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
