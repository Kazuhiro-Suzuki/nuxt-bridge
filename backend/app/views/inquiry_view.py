import logging

from django.forms.models import model_to_dict

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from app.serializers.InquirySerializer import InquirySerializer, InquiryAdminPostSerializer
from app.repositories import inquiry_repositories
from account.repositories import user_repository
from utils import exceptions
from utils.auth import JWTBusinessUserAuthentication, JWTGeneralUserAuthentication, JWTGeneralOrFacilityUserAuthentication

logger = logging.getLogger(__name__)


class InquiryView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralOrFacilityUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        # お問合せの一覧を取得
        user = request.user
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        qs = inquiry_repositories.get_object(user=user, city_code=city_code)
        return Response(data=list(qs.values()), status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        # 新規のお問合せを作成
        user = request.user
        display_name = user.email
        city_code = request.query_params.get('city_code')
        s = InquirySerializer(data=request.data)
        if not s.is_valid():
            logger.error(f'validation error ${request.data}')
            raise exceptions.ValidationException
        object = inquiry_repositories.post_object(city_code, user, user, display_name, **s.validated_data)
        if object:
            for user_profile in user_repository.get_object_list_per_account_type(city_code, 'business'):
                inquiry_repositories.send_email(user_profile.user, city_code)
        return Response(model_to_dict(object), status=status.HTTP_201_CREATED)


class InquiryAdminListView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        # 管理者用に未対応でかつ最も古い問い合わせの問い合わせ日時の昇順の一覧を取得
        city_code = request.query_params.get('city_code')
        qs = inquiry_repositories.get_all_objects(city_code=city_code)
        return Response(data=qs, status=status.HTTP_200_OK)


class InquiryAdminDetailView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request, userId) -> Response:
        # 施設詳細情報を取得
        if not userId:
            raise exceptions.ValidationException
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        qs = inquiry_repositories.get_object(user=userId, city_code=city_code)
        return Response(data=list(qs.values()), status=status.HTTP_200_OK)

    def post(self, request: Request, userId) -> Response:
        # 新規の返信を作成
        user = request.user
        city_code = request.query_params.get('city_code')
        created_to = user_repository.get_object_with_uid(userId)
        s = InquiryAdminPostSerializer(data=request.data)
        if not s.is_valid():
            logger.error(f'validation error ${request.data}')
            raise exceptions.ValidationException
        object = inquiry_repositories.post_object(city_code, user, created_to, **s.validated_data)
        # メール送信
        if object:
            inquiry_repositories.send_email(created_to, city_code)
        return Response(model_to_dict(object), status=status.HTTP_201_CREATED)

    def put(self, request: Request, userId) -> Response:
        # お問合せのステータスを更新
        object = inquiry_repositories.put_object(**request.data)
        return Response(model_to_dict(object), status=status.HTTP_200_OK)
