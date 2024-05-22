import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from account.serializers import token_obtain_serializer
from account.repositories import account_repository

logger = logging.getLogger(__name__)


class TokenObtainView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request) -> Response:
        # flutterアプリから
        if 'from_path' in request.data:
            (token, type, refresh_token) = account_repository.login_without_password(**request.data)
            data = {
                'token': token,
                'type': type,
                'refresh_token': refresh_token,
            }
            return Response(data=data, status=status.HTTP_200_OK)

        # 通常ログイン
        serializer = token_obtain_serializer.TokenObtainSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'TokenObtainSerializer error {request.data}')
            raise exceptions.ValidationException
        
        is_mobile = False
        if 'Device-Token' in request.headers['User-Agent']:
            logger.info(f"User-Agent in Obtain:{request.headers['User-Agent']}")
            is_mobile = True
        
        (token, type, refresh_token) = account_repository.login(is_mobile, **serializer.validated_data)
        data = {
            'token': token,
            'type': type,
            'refresh_token': refresh_token,
        }
        return Response(data=data, status=status.HTTP_200_OK)
