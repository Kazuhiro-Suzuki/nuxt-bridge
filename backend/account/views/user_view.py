import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from account.repositories import account_repository
from app.repositories import firebase_token_repository

logger = logging.getLogger(__name__)


class UserView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        token = account_repository.get_token(headers=dict(request.headers))
        user = account_repository.decode_jwt(token=token)
        if 'Device-Token' in request.headers['User-Agent']:
            firebase_token=request.headers['User-Agent'].split('Device-Token=')[1]
            print('firebase_token:', firebase_token)
            firebase_token_repository.create_or_update_token_object(
                token=firebase_token,
                uid=user.get('user_info').get('uid'),
                city_code=user.get('city_code')
            )
        return Response(data={'user': user}, status=status.HTTP_200_OK)
