import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from account.serializers.request_reset_password_serializer import RequestResetPasswordSerializer
from account.repositories import account_repository

logger = logging.getLogger(__name__)


class RequestResetPasswordView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request):
        serializer = RequestResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'RequestResetPasswordSerializer error {request.data}')
            raise exceptions.ValidationException
        account_repository.send_reset_password_email(**serializer.validated_data)
        return Response(data={}, status=status.HTTP_200_OK)
