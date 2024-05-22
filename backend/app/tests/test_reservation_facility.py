from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import patch


class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code


class ReservationFacilityGetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/app/reservation_facility/'
        self.patcher = patch('app.repositories.reservation_facility_repository.requests.get')
        self.mock_get = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_get_ok(self):
        self.mock_get.side_effect = [MockResponse("""{"id": 1}""", 200)]
        request = self.client.get(self.url, {
            "city_code": "131032",
        })
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.mock_get.assert_called()

    def test_500_get_no_city_code(self):
        request = self.client.get(self.url, {
            'city_code': ''
        })
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_request_error(self):
        self.mock_get.side_effect = [MockResponse("""{"id": 1}""", 500)]
        request = self.client.get(self.url, {
            "city_code": "111111",
        })
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReservationFacilityPostViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/app/reservation_facility/'
        self.patcher = patch('app.repositories.reservation_facility_repository.requests.post')
        self.mock_post = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_post_ok(self):
        self.mock_post.side_effect = [MockResponse("""{"id": 1}""", 200)]
        request = self.client.post(self.url, {
            "city_code": "131032",
        })
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.mock_post.assert_called()

    def test_500_post_request_error(self):
        self.mock_post.side_effect = [MockResponse("""{"id": 1}""", 500)]
        request = self.client.post(self.url, {
            "city_code": "111111",
        })
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReservationFacilityDetailView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/app/reservation_facility/detail/'
        self.patcher = patch('app.repositories.reservation_facility_repository.requests.get')
        self.mock_get = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.patcher.stop()

    def test_200_get_ok(self):
        self.mock_get.side_effect = [MockResponse("""{"id": 1}""", 200)]
        request = self.client.get(self.url, {
            "facilityId": "131032",
        })
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.mock_get.assert_called()

    def test_500_get_no_facilityId(self):
        request = self.client.get(self.url, {
            'facilityId': ''
        })
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_request_error(self):
        self.mock_get.side_effect = [MockResponse("""{"id": 1}""", 500)]
        request = self.client.get(self.url, {
            "facilityId": "111111",
        })
        self.assertEqual(request.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
