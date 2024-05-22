import csv
import os

import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from django.db.models import F
from django.http import HttpResponse

from utils import exceptions
from account.repositories import account_repository,user_repository
from utils.auth import JWTBusinessUserAuthentication


logger = logging.getLogger(__name__)


class UserListView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        if 'city_code' not in request.GET:
            raise exceptions.ValidationException
        city_code = request.GET['city_code']
        queryset = user_repository.get_object_list(city_code=city_code).values(
            'phone_number',
            'fax_number',
            'is_subscribe',
            'is_dangerous').annotate(
            uid=F('user__uid'),
            email=F('user__email'),
            is_active=F('user__is_active'),
            date_joined=F('user__date_joined'),
        )
        return Response(data=list(queryset), status=status.HTTP_200_OK)

    def put(self, request: Request, pk: str) -> Response:
        user_repository.update_status(uid=pk, **request.data)
        return Response(status=status.HTTP_200_OK)

class UserListCsvView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        try:
            token = account_repository.get_token(headers=dict(request.headers))
            user = account_repository.decode_jwt(token=token)
            city_code = request.GET['city_code']
            general_user_profiles = user_repository.get_object_list_per_account_type(city_code=city_code, account_type='general')
            business_user_profiles = user_repository.get_object_list_per_account_type(city_code=city_code, account_type='business')

            data = [
                [
                    'メールアドレス',
                    '電話番号',
                    'FAX番号',
                    '障がい児者との関係',
                    '障がい児者の生年月日',
                    '本人（家族等）の障害種別',
                    '茅ヶ崎市避難行動要支援者支援制度登録要件',
                    '氏',
                    '名',
                    '氏（カナ）',
                    '名（カナ）',
                    'お住まいの地名',
                    '手帳番号（数字のみ）',
                ]
            ]
            for user_profile in general_user_profiles:
                data.append(
                    [   
                        user_profile.email,
                        user_profile.phone_number,
                        user_profile.fax_number,
                        user_profile.user_type,
                        user_profile.birthday,
                        ', '.join(user_profile.disability_type),
                        ', '.join(user_profile.disability_category),
                        user_profile.last_name,
                        user_profile.first_name,
                        user_profile.kana_last_name,
                        user_profile.kana_first_name,
                        user_profile.address_block,
                        user_profile.disablity_number,
                    ] 
                )
            
            temp_file_path = './user-list.csv'
            with open(temp_file_path, 'w', encoding="utf_8_sig") as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                writer.writerows(data)

            with open(temp_file_path, 'r') as csv_file:
                csv_content = csv_file.read()
            
            os.remove(temp_file_path)

            response = HttpResponse(
                content=csv_content,
                content_type='text/csv; charset=utf_8_sig',
                headers={"Content-Disposition": 'attachment; filename="user-list.csv"'},
            )
            for user_profile in business_user_profiles:
                user_repository.send_csv_download_email(informed_email=user['email'], user=user_profile.user, city_code=city_code)
            return response
        except Exception as e:
            logger.error(e)
            raise exceptions.Exception500

class FacilityUserListView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTBusinessUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        if 'city_code' not in request.GET:
            raise exceptions.ValidationException
        city_code = request.GET['city_code']
        data = []
        user_profiles = user_repository.get_object_list_per_account_type(city_code=city_code, account_type='facility')
        for user_profile in user_profiles:
            facilities = user_profile.user.facilitymanger_set.all().annotate(id=F('facility__id'), name=F('facility__name')).values('id', 'name')
            facility_user = {
                'is_subscribe': user_profile.is_subscribe,
                'is_dangerous': user_profile.is_dangerous,
                'uid': user_profile.user.uid,
                'email': user_profile.user.email,
                'is_active': user_profile.user.is_active,
                'date_joined': user_profile.user.date_joined,
                'facilities': []
            }
            for facility in facilities:
                facility_user['facilities'].append(facility)
            data.append(facility_user)
        return Response(data=data, status=status.HTTP_200_OK)
