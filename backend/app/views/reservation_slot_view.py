import logging
from datetime import datetime
from utils import exceptions

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from app.repositories import reservation_slot_repository as rsr
from app.utils.list_util import fetch_dict_or_List
from utils.auth import JWTGeneralUserAuthentication

logger = logging.getLogger(__name__)


class ReservationSlotView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request):
        # 予約枠の詳細を取得
        if not (slotId := request.GET['slotId'].split(',')):
            logger.error(f'ReservationSlotView get error {request}')
            raise exceptions.ValidationException
        
        city_code = ''
        if 'city_code' in request.GET:
            city_code = request.GET['city_code']

        response = rsr.get_slot(slotId=slotId, city_code=city_code)
        return Response(data=fetch_dict_or_List(response), status=status.HTTP_200_OK)

    def post(self, request: Request):
        # 条件を指定して予約枠の一覧が欲しい
        if 'citycode' not in request.data:
            logger.error(f'ReservationSlotView post error {request.data}')
            raise exceptions.ValidationException
        city_code = request.data['citycode']

        facility_id = ''
        if 'facilityId' in request.data:
            facility_id = request.data['facilityId']

        menu_id = ''
        if 'menuId' in request.data:
            menu_id = request.data['menuId']

        start_date = ''
        if 'startDate' in request.data:
            try:
                start_date = request.data['startDate']
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError as e:
                logger.error(f'ReservationSlotView post error {request} {e}')
                raise exceptions.ValidationException

        end_date = ''
        if 'endDate' in request.data:
            try:
                end_date = request.data['endDate']
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError as e:
                logger.error(f'ReservationSlotView post error {request} {e}')
                raise exceptions.ValidationException

        response = rsr.find_slot(city_code, facility_id, menu_id, start_date, end_date)

        return Response(data=response, status=status.HTTP_200_OK)
