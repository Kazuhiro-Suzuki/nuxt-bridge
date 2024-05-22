import logging
from utils import exceptions

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from app.serializers.slot_serializer import SlotSerializer
from app.repositories import reservation_slot_repository as rsr
from utils.auth import JWTGeneralUserAuthentication

logger = logging.getLogger(__name__)


class ReservationSlotNativeView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request: Request):
        # 条件を指定して予約枠をGET
        serializer = SlotSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'SlotSerializer error ${request.data}')
            raise exceptions.ValidationException
        slots = rsr.find_slot_native(**serializer.validated_data)
        return Response(data=slots, status=status.HTTP_200_OK)
