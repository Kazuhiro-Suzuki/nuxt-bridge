import logging

from django.forms.models import model_to_dict
from django.db.models import F


from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from app.serializers.facility_serializer import FacilitySerializer
from app.repositories import facility_repositories, fcs_repositories
from utils import exceptions
from utils.auth import JWTBusinessUserAuthentication

logger = logging.getLogger(__name__)


class FacilityView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request: Request) -> Response:
        serializer = FacilitySerializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationException
        try:
            facility = facility_repositories.post_object(**serializer.validated_data)
            fcs_facility = fcs_repositories.post_fcs_object(facility)
            facility_repositories.update_facility_list_cash(city_code=serializer.validated_data.get('city_code'))
            return Response(model_to_dict(facility), status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            if facility is not None:
                facility_repositories.delete_object(facility.id)
            if fcs_facility is not None:
                fcs_repositories.delete_fsc_object(facility)
            return Response(data={'detail': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, pk: int) -> Response:
        if not pk:
            raise exceptions.ValidationException
        serializer = FacilitySerializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationException
        try: 
            # facility = facility_repositories.put_object(request.data)
            facility = facility_repositories.put_object(pk, serializer.validated_data)
            fcs_facility = fcs_repositories.put_fcs_object(facility)
            return Response(model_to_dict(facility), status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response(data={'detail': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, pk: int) -> Response:
        if not pk:
            raise exceptions.ValidationException
        try:
            facility = facility_repositories.get_public_object_by_id(pk)
            fcs_repositories.delete_fcs_object(facility)
            facility_repositories.delete_object(pk)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
        return Response(data={'detail': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FacilityPublicView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if 'facility_id' in request.GET:
            qs = facility_repositories.get_public_object_by_id(facility_id=request.GET.get('facility_id'))
            return Response(data=model_to_dict(qs), status=status.HTTP_200_OK)
        if not (city_code := request.GET.get('city_code')) or not(facility_type := request.GET.get('facility_type')):
            raise exceptions.ValidationException
        qs = facility_repositories.get_public_object(city_code=city_code, facility_type=facility_type)
        return Response(data=qs, status=status.HTTP_200_OK)


class FacilityAllPublicView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        qs = facility_repositories.get_all_public_object(city_code=city_code).select_related('region').values(
            'id', 
            'name', 
            city_code=F('region__city_code'))
        return Response(data=list(qs), status=status.HTTP_200_OK)
