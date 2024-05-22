import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from account.serializers import token_refresh_serializer
from account.repositories import account_repository

logger = logging.getLogger(__name__)


class TokenRefreshView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request) -> Response:
        serializer = token_refresh_serializer.TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            # logger.warning(f'TokenRefreshSerializer warning {request.data}')
            raise exceptions.ValidationException
        
        is_mobile = False
        if 'Device-Token' in request.headers['User-Agent']:
            logger.info(f"User-Agent in Refresh:{request.headers['User-Agent']}")
            is_mobile = True
        
        token, refresh_token = account_repository.get_refresh_jwt(is_mobile, **serializer.validated_data)
        data = {
            'token': token,
            'refresh_token': refresh_token
        }
        return Response(data=data, status=status.HTTP_200_OK)
