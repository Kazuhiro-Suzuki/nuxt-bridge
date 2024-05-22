import logging
from config import settings

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from app.repositories import reservation_facility_repository as rfr

logger = logging.getLogger(__name__)


class ReservationFacilityView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        # 自治体の施設情報一覧を取得
        if not (city_code := request.GET['city_code']):
            raise exceptions.ValidationException
        facilities = rfr.get_objects(city_code=city_code)
        return Response(data=facilities, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        # 施設情報を検索
        city_code = ''
        if 'city_code' in request.GET:
            city_code = request.GET['city_code']
        
        facilities = rfr.find_facility(city_code=city_code)
        return Response(data=facilities, status=status.HTTP_200_OK)


class ReservationFacilityDetailView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        # 施設詳細情報を取得
        if not (facilityId := request.GET['facilityId']):
            raise exceptions.ValidationException

        city_code = ''
        if 'city_code' in request.GET:
            city_code = request.GET['city_code']

        facility = rfr.get_facility_detail(city_code=city_code,facility_id=facilityId)
        return Response(data=facility, status=status.HTTP_200_OK)
