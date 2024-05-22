import logging
from wsgiref import validate

from config import settings
from django.forms.models import model_to_dict

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from app.repositories import notification_repositories, uploaded_file_repository
from app.serializers.notification_serializer import NotificationSerializer
from app.utils.dict_util import replace_api_with_domain
from utils import exceptions
from utils.auth import JWTBusinessUserAuthentication, JWTAppUserAuthentication

logger = logging.getLogger(__name__)


class NotificationView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        if 'city_code' not in request.GET:
            raise exceptions.ValidationException
        city_code = request.GET['city_code']
        qs = notification_repositories.get_object(city_code=city_code)
        return Response(data=list(qs.values()), status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        s = NotificationSerializer(data=request.data)
        if not s.is_valid():
            logger.error(f'validation error ${request.data}')
            raise exceptions.ValidationException
        notification = notification_repositories.post_object(s.validated_data)
        if (file_ids :=  request.data.get('file_ids')) and (city_code := request.data.get('city_code')):
            uploaded_files = uploaded_file_repository.get_object(file_ids)
            notification_repositories.create_notification_file(city_code=city_code, instance=notification, files=uploaded_files)
        return Response(model_to_dict(notification), status=status.HTTP_201_CREATED)

    

class NotificationDetailView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        notification = notification_repositories.get_object_by_id(pk)
        #SITE_DOMAINを画像URLの前に付与する
        data = replace_api_with_domain(settings.BASE_URL, [model_to_dict(notification)])
        return Response(data=data, status=status.HTTP_200_OK)

    
    def put(self, request: Request, pk: int) -> Response:
        notification = notification_repositories.put_object(request.data)
        if file_ids :=  request.data.get('file_ids'):
            uploaded_files = uploaded_file_repository.get_object(file_ids)
            notification_repositories.create_notification_file(notification, uploaded_files)
        return Response(model_to_dict(notification), status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int) -> Response:
        if not pk:
            raise exceptions.ValidationException
        notification_files = notification_repositories.get_file_ids_by_notification(pk)
        notification = notification_repositories.delete_object(pk)
        logger.info(f'{notification} deleted')
        if notification_files:
            uploaded_file = uploaded_file_repository.delete_object(notification_files)
            logger.info(f'{uploaded_file} deleted')
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class NotificationPublicView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTAppUserAuthentication]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        qs = notification_repositories.get_public_object_per_user(user=request.user,city_code=city_code)
        #SITE_DOMAINを画像URLの前に付与する
        data = replace_api_with_domain(settings.BASE_URL, qs.values())
        return Response(data=data, status=status.HTTP_200_OK)

