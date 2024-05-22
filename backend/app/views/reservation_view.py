import logging
from config import settings

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from utils import exceptions
from app.repositories import reservation_repository as rr
from app.utils.list_util import convert_to_list, fetch_dict_or_List
from utils.auth import JWTGeneralUserAuthentication

logger = logging.getLogger(__name__)


class ReservationView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request: Request) -> Response:
        # 予約を実行
        if not (email := request.data['email']) \
                or not (temporaryReservationId := request.data['temporaryReservationId'])\
                or not (surveyResponse :=  request.data['surveyResponse']):
            logger.error(f'ReservationView post error {request}')
            raise exceptions.ValidationException
        response = rr.create_reservation(email=email, temporaryReservationId=convert_to_list(temporaryReservationId), surveyResponse=surveyResponse)
        return Response(data=fetch_dict_or_List(response), status=status.HTTP_201_CREATED)

    def put(self, request: Request, pk: str) -> Response:
        # 予約をキャンセル
        if not (request.data['email']) or not pk:
            logger.error(f'ReservationView put error {request}')
            raise exceptions.ValidationException
        response = rr.cancel_reservation(
            email=request.data['email'],
            reservation_id=pk
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        # ユーザの予約情報を取得
        if 'uid' not in request.GET:
            logger.error(f'ReservationView get error {request.GET}')
            raise exceptions.ValidationException
        uid = request.user.uid

        reservation_id = []
        if 'reservationId' in request.GET:
            reservation_id = request.GET['reservationId'].split(',')

        response = rr.get_reservation(uid=uid, reservation_id=reservation_id)
        return Response(data=response, status=status.HTTP_200_OK)
