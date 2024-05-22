import boto3
import logging

from config import settings

from django.http import HttpResponse
from django.utils.cache import patch_response_headers

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg





logger = logging.getLogger(__name__)


class InformationFileView(APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request: Request) -> Response:
        name = request.query_params.get('name')
        try:
            # s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            #             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3 = boto3.resource('s3')
            file = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, key=f'information-files/chigasaki/{name}').get()
            response = HttpResponse(file['Body'].read(), content_type=file['ContentType'])
            patch_response_headers(response, cache_timeout=3600)
            return response
        except Exception as e:
            logger.error(format_error_single_line(e))
            raise exceptions.Exception500(ErrMsg.FAILED_GET_FILE)
