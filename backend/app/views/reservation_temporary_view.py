import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from utils import exceptions
from utils.auth import JWTGeneralUserAuthentication
from app.repositories import reservation_temporary_repository as rtr
from app.utils.list_util import fetch_dict_or_List, convert_to_list

logger = logging.getLogger(__name__)


class ReservationTemporaryView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request: Request) -> Response:
        # 仮予約を実行
        if not (email := request.data['email']) or not (slot_id := request.data['slotId']):
            logger.error(f'ReservationTemporaryView post error {request}')
            raise exceptions.ValidationException
        response = rtr.post_reservation_temporary(
            email=email,
            slot_id=convert_to_list(slot_id)
        )
        return Response(data=fetch_dict_or_List(response), status=status.HTTP_201_CREATED)

    def put(self, request: Request, pk: str = '') -> Response:
        # 仮予約をキャンセル
        if not (email := request.data['email']) or not (temporary_reservation_id := request.GET['reservationTemporaryId'].split(',') or not (temporary_reservation_id := pk)):
            logger.error(f'ReservationTemporaryView put error {request}')
            raise exceptions.ValidationException
        response = rtr.cancel_reservation_temporary(
            email=email,
            temporary_reservation_id= convert_to_list(temporary_reservation_id),
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        # ユーザの仮予約情報を取得
        if not (email := request.GET['email']):
            logger.error(f'ReservationTemporaryView get error {request}')
            raise exceptions.ValidationException
        response = rtr.get_reservation_temporary(email=email)
        return Response(data=response, status=status.HTTP_200_OK)
