from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from account.repositories import account_repository
from app.models.region import Region
from app.models.notification import Notification
from app.views.notification_view import NotificationView, NotificationPublicView


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

    Notification.objects.create(
        subject='お知らせ題名1',
        body='お知らせ本文1',
        is_active=True,
        active_since='2021-02-21 06:35:45.707450',
        region_id=region.id,
    )

    return user, token


class NotificationViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.url = '/api/v1/app/notification/'
        self.client = APIRequestFactory()
        self.view = NotificationView.as_view()

    def test_200_get_ok(self):
        request = self.client.get(self.url, {
            "city_code": "131032",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_500_get_invalid_city_code(self):
        request = self.client.get(self.url, {
            "city_code": "111111",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_no_city_code(self):
        request = self.client.get(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_201_post_ok(self):
        request = self.client.post(self.url, {
            "subject": 'お知らせ題名2',
            "body": 'お知らせ本文2',
            "city_code": '131032',
            "active_since": '2013-02-21 06:35:45.707450',
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_500_post_serializer_error(self):
        request = self.client.post(self.url, {
            "subject": 'お知らせ題名2',
            "body": 'お知らせ本文2',
            "city_code": '131032',
            "active_since": '2013-02-21',
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_post_invalid_city_code(self):
        request = self.client.post(self.url, {
            "subject": 'お知らせ題名2',
            "body": 'お知らせ本文2',
            "city_code": '111111',
            "active_since": '2013-02-21 06:35:45.707450',
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_200_put_ok(self):
        request = self.client.put(self.url + '1/', {
            'id': '1',
            'subject': 'お知らせ題名-update',
            'body': 'お知らせ本文-update',
            'active_since': '2021-02-21 06:35:45.707450',
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_500_put_invalid_pk(self):
        request = self.client.put(self.url + '2/', {
            'id': '2',
            'subject': 'お知らせ題名-update',
            'body': 'お知らせ本文-update',
            'active_since': '2021-02-21 06:35:45.707450',
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_204_delete_ok(self):
        request = self.client.delete(self.url + '1/')
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_500_delete_invalid_pk(self):
        request = self.client.delete(self.url + '1/')
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_delete_no_pk(self):
        request = self.client.delete(self.url + '1/')
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk='')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotificationPublicViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.url = '/api/v1/app/notification/public/'
        self.client = APIRequestFactory()
        self.view = NotificationPublicView.as_view()

    def test_200_get_ok(self):
        request = self.client.get(self.url, {
            "city_code": "131032",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_500_get_invalid_city_code(self):
        request = self.client.get(self.url, {
            "city_code": "11111",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_no_city_code(self):
        request = self.client.get(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
