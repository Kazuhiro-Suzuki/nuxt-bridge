import os
import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from account.repositories import account_repository
from account.repositories import city_ca_repository
from account.repositories import user_city_ca_repository
from account.serializers import signup_serializer
from app.models.region import Region
from app.repositories import reservation_connection_repository


DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']
logger = logging.getLogger(__name__)


class SignUpView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request):
        """
        1. 本アプリ側でUserを作成
        2. CityCa側にユーザ情報をポスト
        3. 本アプリ側でUserCityCaを作成
        4. アカウント有効化リンクのメールを送信する
        """
        serializer = signup_serializer.SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'SignUpSerializer error {request.data}')
            raise exceptions.ValidationException
        user, user_ca = None, None
        citycode = serializer.validated_data['city_code']
        try:
            user, user_profile = account_repository.create_account(serializer.validated_data)
            is_reservation_active = reservation_connection_repository.check_reservation_active(city_code=citycode)
            if DJANGO_SETTINGS_MODULE != 'config.settings_local':
                if is_reservation_active:
                    user_ca = city_ca_repository.create_account_city_ca(user_profile=user_profile)
                    user_city_ca_repository.create_user_city_ca(user=user, uid=user_ca['uuid'], city_code=citycode)
                account_repository.send_create_account_email(user=user, city_code=citycode)
            return Response(data={'user': user.email}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            if user_ca is not None:
                city_ca_repository.delete_account_city_ca(uuid=user_ca['uuid'])
            if user is not None:
                account_repository.delete_account(user=user, user_profile=user_profile)
            return Response(data={'detail': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpFacilityUserView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request):
        """
        本アプリ側でUserとUserProfileを作成
        Passwordを自動生成
        """
        password = account_repository.generate_password(8)
        request.data['password'] = password
        request.data['password_reconfirm'] = password
        serializer = signup_serializer.SignUpFacilityUserSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'SignUpFacilityUserSerializer error {request.data}')
            raise exceptions.ValidationException
        user = None
        try:
            user, user_profile = account_repository.create_account(serializer.validated_data)
            facility_managers = account_repository.create_facility_manager(
                city_code=request.data['city_code'], 
                user=user, 
                facilities=request.data['facilities']
            )
            return Response(
                data={'email': user.email, 'password': password, 'name': [facility_manager.facility.name for facility_manager in facility_managers]}, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(e)
            if user is not None:
                account_repository.delete_account(user=user, user_profile=user_profile)
            return Response(data={'detail': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)