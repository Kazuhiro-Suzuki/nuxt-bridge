import logging

from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from utils import exceptions


from app.repositories import uploaded_file_repository
from utils.auth import JWTBusinessUserAuthentication


logger = logging.getLogger(__name__)

class UploadFileView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [MultiPartParser]

    def post(self, request: Request, format=None) -> Response:
        if not (files := request.FILES.getlist('files')) \
                or not(city_code := request.data.get('city_code')) \
                or not(visible_scope := request.data.get('visible_scope')):
            raise exceptions.ValidationException
        uploaded_files = uploaded_file_repository.save_object(city_code, files, request.user, visible_scope)
        return Response(data=uploaded_files, status=status.HTTP_201_CREATED)


class UploadFilePublicView(APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request: Request) -> Response:
        file_id = request.query_params.get('file_id')
        file = uploaded_file_repository.get_object_from_s3(file_id, request.user)
        return HttpResponse(file['Body'].read(), content_type=file['ContentType'])