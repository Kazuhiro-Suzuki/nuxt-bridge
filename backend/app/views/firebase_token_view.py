import logging

from django.forms.models import model_to_dict

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from app.repositories import firebase_token_repository
from utils import exceptions

logger = logging.getLogger(__name__)


class FirebaseTokenView(APIView):
    renderer_classes = [JSONRenderer, ]
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request) -> Response:
        if not(token := request.data.get('token')) or not (city_code := request.data.get('city_code')):
            logger.error(f'FirebaseTokenView POST error {request.data}')
            raise exceptions.ValidationException
        firebase_token_repository.create_token_object(
            token=token,
            city_code=city_code
        )
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        if not(city_code := request.GET.get('city_code')):
            logger.error(f'FirebaseTokenView GET error {request.data}')
            raise exceptions.ValidationException
        objects = firebase_token_repository.get_token_objects(city_code=city_code)
        return Response(data=model_to_dict(objects), status=status.HTTP_200_OK)


class FirebaseTokenVerifyView(APIView):
    renderer_classes = [JSONRenderer, ]
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request) -> Response:
        if not(token := request.data.get('token')):
            logger.error(f'FirebaseTokenVerifyView POST error {request.data}')
            raise exceptions.ValidationException
        result = firebase_token_repository.verify_token(token=token)
        return Response(data={'result': result}, status=status.HTTP_200_OK)
