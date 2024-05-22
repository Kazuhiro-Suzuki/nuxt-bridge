import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from app.repositories import faq_repository

logger = logging.getLogger(__name__)


class FAQView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if 'city_code' not in request.GET:
            raise exceptions.ValidationException
        qs = faq_repository.get_object_with_category(city_code=request.GET['city_code'])
        return Response(data=qs, status=status.HTTP_200_OK)
        # return Response(data=list(qs.values()), status=status.HTTP_200_OK)
