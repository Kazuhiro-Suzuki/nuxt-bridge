from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from django.forms.models import model_to_dict

from app.models.reservation import ReservationConnection
from app.repositories import reservation_connection_repository as rcr
from app.utils.dict_util import dataclass_as_dict


class ReservationConnectionView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        # 自治体からのメッセージ一覧を取得
        if not (city_code := request.GET['city_code']):
            raise exceptions.ValidationException
        reservation_connection = rcr.get_reservation_conection(city_code=city_code)
        return Response(data=model_to_dict(reservation_connection), status=status.HTTP_200_OK)
