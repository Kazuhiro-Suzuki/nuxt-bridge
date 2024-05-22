from django.forms.models import model_to_dict

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from utils import exceptions
from app.repositories import region_repositories


class RegionView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        qs = region_repositories.get_object(city_code=city_code)
        return Response(data=model_to_dict(qs), status=status.HTTP_200_OK)
