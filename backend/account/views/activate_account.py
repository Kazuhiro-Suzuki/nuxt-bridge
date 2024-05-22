import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from account.serializers import activate_account_serializer
from account.repositories import account_repository

logger = logging.getLogger(__name__)


class ActivateAccount(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request):
        serializers = activate_account_serializer.ActivateAccountSerializer(data=request.data)
        if not serializers.is_valid():
            logger.error(f'ActivateAccountSerializer error {request.data}')
            raise exceptions.ValidationException
        account_repository.activate_account(**serializers.validated_data)
        return Response(status=status.HTTP_200_OK)
