from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from unittest.mock import patch

from account.models.user_city_ca import UserCityCa
from account.repositories import account_repository
from app.views.reservation_view import ReservationView

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
        self.view = ReservationView.as_view()
        self.url = '/api/v1/app/reservation/'
        self.patcher = patch('app.repositories.reservation_repository.requests.post')
        self.mock_post = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_post_ok(self):
        self.mock_post.side_effect = [MockResponse("""{"customerUuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 200)]
        request = self.client.post(self.url, {
            "email": "test-user@gmail.com",
            "temporaryReservationId": '1',
            "surveyResponse": [{'questionId': '1'}]
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.mock_post.assert_called()

    def test_500_post_no_value(self):
        self.mock_post.side_effect = [MockResponse("""{"customerUuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 200)]
        request = self.client.post(self.url, {
            "email": "test-user@gmail.com",
            "temporaryReservationId": '',
            "surveyResponse": []
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_post_request_error(self):
        self.mock_post.side_effect = [MockResponse("""{"customerUuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 500)]
        request = self.client.post(self.url, {
            "email": "test-user@gmail.com",
            "temporaryReservationId": '1',
            "surveyResponse": [{'questionId': '1'}]
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.mock_post.assert_called()


class ReservationGetViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.client = APIRequestFactory()
        self.view = ReservationView.as_view()
        self.url = '/api/v1/app/reservation/'
        self.patcher = patch('app.repositories.reservation_repository.requests.post')
        self.mock_get = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_get_ok(self):
        self.mock_get.side_effect = [MockResponse("""{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 200)]
        request = self.client.get(self.url, {
            "uid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "reservationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_get.assert_called()

    def test_500_get_no_uid(self):
        self.mock_get.side_effect = [MockResponse("""{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 200)]
        request = self.client.get(self.url)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_no_reservation_id(self):
        self.mock_get.side_effect = [MockResponse("""{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 200)]
        request = self.client.get(self.url, {
            "uid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_500_get_request_error(self):
        self.mock_get.side_effect = [MockResponse("""{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 500)]
        request = self.client.get(self.url, {
            "uid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.mock_get.assert_called()


class ReservationPutViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.client = APIRequestFactory()
        self.view = ReservationView.as_view()
        self.url = '/api/v1/app/reservation/'
        self.patcher = patch('app.repositories.reservation_repository.requests.post')
        self.mock_put = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_put_ok(self):
        self.mock_put.side_effect = [MockResponse("""{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 200)]
        request = self.client.put(self.url+'3fa85f64-5717-4562-b3fc-2c963f66afa6/', {
            "email": "test-user@gmail.com",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk='3fa85f64-5717-4562-b3fc-2c963f66afa6')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_put.assert_called()

    def test_500_put_no_email(self):
        self.mock_put.side_effect = [MockResponse("""{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 200)]
        request = self.client.put(self.url+'3fa85f64-5717-4562-b3fc-2c963f66afa6/', {
            "email": "",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk='3fa85f64-5717-4562-b3fc-2c963f66afa6')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_put_request_error(self):
        self.mock_put.side_effect = [MockResponse("""{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}""", 500)]
        request = self.client.put(self.url+'3fa85f64-5717-4562-b3fc-2c963f66afa6/', {
            "email": "test-user@gmail.com",
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request, pk='3fa85f64-5717-4562-b3fc-2c963f66afa6')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.mock_put.assert_called()
