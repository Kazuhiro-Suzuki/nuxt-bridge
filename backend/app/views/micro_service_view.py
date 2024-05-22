from django.forms.models import model_to_dict

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from utils import exceptions
from app.models.micro_service_connection import MicroServiceConnection
from app.repositories import region_repositories


class MicroServiceView(APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        region = region_repositories.get_object(city_code=city_code)
        qs = MicroServiceConnection.objects.get(region=region)
        return Response(data=model_to_dict(qs), status=status.HTTP_200_OK)