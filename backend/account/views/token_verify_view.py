import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from account.repositories import account_repository

logger = logging.getLogger(__name__)


class TokenVerifyView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request) -> Response:
        token = account_repository.get_token(headers=dict(request.headers))
        data = account_repository.decode_jwt(token=token)
        return Response(data=data, status=status.HTTP_200_OK)

