import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from account.repositories import account_repository
from account.serializers.reset_password_serializer import ResetPasswordSerializer

logger = logging.getLogger(__name__)


class ResetPasswordView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'ResetPasswordSerializer error {request.data}')
            raise exceptions.ValidationException
        account_repository.update_password(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
