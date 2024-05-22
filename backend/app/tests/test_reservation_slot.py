from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from unittest.mock import patch

from account.models.user_city_ca import UserCityCa
from account.repositories import account_repository
from app.views.reservation_slot_view import ReservationSlotView

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


class ReservationTemporaryGetViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.client = APIRequestFactory()
        self.view = ReservationSlotView.as_view()
        self.url = '/api/v1/app/reservation_slot/'
        self.patcher = patch('app.repositories.reservation_slot_repository.requests.get')
        self.mock_get = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_get_ok(self):
        self.mock_get.side_effect = [MockResponse("""{"id": "0"}""", 200)]
        request = self.client.get(self.url, {
            "slotId": "1",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_get.assert_called()

    def test_200_get_no_slot_id(self):
        self.mock_get.side_effect = [MockResponse("""{"id": "0"}""", 200)]
        request = self.client.get(self.url, {
            "slotId": "",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_request_error(self):
        self.mock_get.side_effect = [MockResponse("""{"id": "0"}""", 500)]
        request = self.client.get(self.url, {
            "slotId": "1",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.mock_get.assert_called()


class ReservationPostViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.client = APIRequestFactory()
        self.view = ReservationSlotView.as_view()
        self.url = '/api/v1/app/reservation_slot/'
        self.patcher = patch('app.repositories.reservation_slot_repository.requests.post')
        self.mock_post = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_post_ok(self):
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'menuId': '0',
            'startDate': '2021-11-18',
            'endDate': '2021-11-18'
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_post.assert_called()

    def test_500_requests_post_request_error(self):
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 500)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'menuId': '0',
            'startDate': '2021-11-18',
            'endDate': '2021-11-18'
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.mock_post.assert_called()

    def test_500_post_no_city_code(self):
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'facilityId': '1',
            'menuId': '0',
            'startDate': '2021-11-18',
            'endDate': '2021-11-18'
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_200_post_only_city_code(self):
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_post.assert_called()

    def test_500_post_invalid_start_date(self):
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'menuId': '0',
            'startDate': 'date',
            'endDate': '2021-11-18'
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_post_invalid_end_date(self):
        self.mock_post.side_effect = [MockResponse("""[{"id": 0, "cityCode": "012084"}]""", 200)]
        request = self.client.post(self.url, {
            'citycode': '1',
            'facilityId': '1',
            'menuId': '0',
            'startDate': '2021-11-18',
            'endDate': 'date'
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
