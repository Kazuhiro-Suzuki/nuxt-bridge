from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from unittest.mock import patch

from account.models.user_city_ca import UserCityCa
from account.repositories import account_repository
from app.views.reservation_slot_customize_view import ReservationSlotCustomizeView

User = get_user_model()


def set_up_test_data():
    user = User.objects.create_user(
        email='test-user@gmail.com',
        password='test',
        phone_number='123456',
        type='general_user'
    )
    UserCityCa.objects.create(
        user=user,
        uid='3fa85f64-5717-4562-b3fc-2c963f66afa6',
    )

    (token, _, _) = account_repository.generate_jwt(
        email=user.email,
        type=user.type,
        city_code='131032'
    )

    return user, token


class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code


class ReservationPostViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.client = APIRequestFactory()
        self.view = ReservationSlotCustomizeView.as_view()
        self.url = '/api/v1/app/reservation_slot_customize/'
        self.patcher_get = patch('app.repositories.reservation_slot_repository.requests.get')
        self.patcher_post = patch('app.repositories.reservation_slot_repository.requests.post')
        self.mock_get = self.patcher_get.start()
        self.mock_post = self.patcher_post.start()
        self.addCleanup(self.patcher_get.stop)
        self.addCleanup(self.patcher_post.stop)

    def tearDown(self):
        self.patcher_get.stop()
        self.patcher_post.stop()

    def test_200_post_ok(self):
        self.mock_get.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'weekCount': 1,
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_get.assert_called()
        self.mock_post.assert_called()

    def test_500_post_no_city_code(self):
        self.mock_get.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'facilityId': '1',
            'weekCount': 1,
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_post_no_facility_id(self):
        self.mock_get.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'weekCount': 1,
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_post_no_week_count(self):
        self.mock_get.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_get.assert_called()
        self.mock_post.assert_called()

    def test_500_requests_get_request_error(self):
        self.mock_get.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 500)]
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'weekCount': 2,
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.mock_get.assert_called()

    def test_500_no_menu(self):
        self.mock_get.side_effect = [MockResponse("""[]""", 200)]
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'weekCount': 2,
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_get.assert_called()

    def test_500_requests_post_request_error(self):
        self.mock_get.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 500)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'weekCount': 2,
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.mock_get.assert_called()
