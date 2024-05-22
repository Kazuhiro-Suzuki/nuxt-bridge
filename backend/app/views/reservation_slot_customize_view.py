import logging
from datetime import timezone, timedelta, datetime

from rest_framework import permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.auth import JWTGeneralUserAuthentication
from utils import exceptions
from app.repositories import reservation_slot_repository as rsr

logger = logging.getLogger(__name__)


class ReservationSlotCustomizeView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request: Request):
        # 予約枠画面専用の予約枠一覧を取得
        if 'citycode' not in request.data:
            logger.error(f'ReservationSlotCustomizeView post error {request.data}')
            raise exceptions.ValidationException
        city_code = request.data['citycode']

        if 'facilityId' not in request.data:
            logger.error(f'ReservationSlotCustomizeView post error {request.data}')
            raise exceptions.ValidationException
        facility_id = request.data['facilityId']

        jst_timezone = timezone(timedelta(hours=+9), 'JST')
        target_date = datetime.now(jst_timezone)
        if 'weekCount' not in request.data:
            start_date = target_date
            end_date = (target_date + timedelta(days=6))
        else:
            target_date = target_date + timedelta(weeks=request.data['weekCount'])
            start_date = target_date
            end_date = (target_date + timedelta(days=6))

        response = rsr.find_customize_slot(city_code, facility_id, start_date, end_date)
        return Response(data=response, status=status.HTTP_200_OK)
