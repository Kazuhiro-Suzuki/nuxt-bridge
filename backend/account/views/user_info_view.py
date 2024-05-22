import logging
import uuid

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from django.db.models import F
from django.http import HttpResponse

from account.repositories import account_repository, user_repository, city_ca_repository, user_city_ca_repository
from account.serializers.user_info_serializer import UserInfoSerializer
from app.repositories import reservation_connection_repository
from utils import exceptions
from utils.auth import JWTAppUserAuthentication

logger = logging.getLogger(__name__)


class UserInfoView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTAppUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: Request) -> Response:
        token = account_repository.get_token(headers=dict(request.headers))
        user = account_repository.decode_jwt(token=token)
        is_reservation_active = reservation_connection_repository.check_reservation_active(city_code=user['city_code'])
        if (user['type'] == 'general'):
            if is_reservation_active:
                (user_info, user_ca_info) = user_repository.get_object_with_ca(email=user['email'])
            else:
                user_info, user_ca_info = user_repository.get_profile(email=user['email']), ''
            data = {
                'uid': user_info.uid,
                'email': user_info.email,
                'phone_number': user_info.phone_number,
                'fax_number': user_info.fax_number,
                'age': user_info.age,
                'age_range': user_info.age_range,
                'type': user_info.account_type,
                'ca_uid': user_ca_info.uid if user_ca_info else '',
                'kana_last_name': user_info.kana_last_name,
                'kana_first_name': user_info.kana_first_name,
                'last_name': user_info.last_name,
                'first_name': user_info.first_name,
                'user_type': user_info.user_type,
                'user_type_detail': user_info.user_type,
                'birthday': user_info.birthday,
                'postal_code_1': user_info.postal_code_1,
                'postal_code_2': user_info.postal_code_2,
                'address_prefecture': user_info.address_prefecture,
                'address_city': user_info.address_city,
                'address_block': user_info.address_block,
                'disability_type': user_info.disability_type,
                'disablity_grade': user_info.disablity_grade,
                'disablity_prefecture':  user_info.disablity_prefecture,
                'disablity_number':  user_info.disablity_number,
                'disability_category':  user_info.disability_category,
                'notification_tag': user_info.notification_tag,
                'note1': user_info.note1,
                'note2': user_info.note2,
                'note3': user_info.note3,
                'expire_date1': user_info.expire_date1,
                'expire_date2': user_info.expire_date2,
                'expire_date3': user_info.expire_date3,
                'expire_date4': user_info.expire_date4,
                'expire_date5': user_info.expire_date5,
                'expire_date6': user_info.expire_date6,
                'expire_date7': user_info.expire_date7,
                'is_subscribe': user_info.is_subscribe,
                'get_notification': user_info.get_notification,
                'get_disaster_notification': user_info.get_disaster_notification,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            user_obj = user_repository.get_object(email=user['email'])
            user_profile = user_obj.partitioneduserprofile_set.get()

            # facility = None
            # if user_profile.facility:
            #     facility = user_profile.facility.name
            
            data = {
                'uid': user_obj.uid,
                'email': user_obj.email,
                'type': user_profile.account_type,
                'age': user_profile.age,
                'age_range': user_profile.age_range,
                'ca_uid': '',
                'kana_last_name': user_profile.kana_last_name,
                'kana_first_name': user_profile.kana_first_name,
                'last_name': user_profile.last_name,
                'first_name': user_profile.first_name,
                'user_type': user_profile.user_type,
                'user_type_detail': user_profile.user_type,
                'facilities': [],
                'birthday': user_profile.birthday,
                'postal_code_1': user_profile.postal_code_1,
                'postal_code_2': user_profile.postal_code_2,
                'address_prefecture': user_profile.address_prefecture,
                'address_city': user_profile.address_city,
                'address_block': user_profile.address_block,
                'disability_type': user_profile.disability_type,
                'disablity_grade': user_profile.disablity_grade,
                'disablity_prefecture':  user_profile.disablity_prefecture,
                'disablity_number':  user_profile.disablity_number,
                'disability_category':  user_profile.disability_category,
                'notification_tag': user_profile.notification_tag,
                'note1': user_profile.note1,
                'note2': user_profile.note2,
                'note3': user_profile.note3,
                'expire_date1': user_profile.expire_date1,
                'expire_date2': user_profile.expire_date2,
                'expire_date3': user_profile.expire_date3,
                'expire_date4': user_profile.expire_date4,
                'expire_date5': user_profile.expire_date5,
                'expire_date6': user_profile.expire_date6,
                'expire_date7': user_profile.expire_date7,
                'is_subscribe': user_profile.is_subscribe,
                'get_notification': user_profile.get_notification,
                'get_disaster_notification': user_profile.get_disaster_notification,
            }
            if user_profile.phone_number is not None:
                data['phone_number'] = user_profile.phone_number
            else:
                data['phone_number'] = ''

            if user_profile.fax_number is not None:
                data['fax_number'] = user_profile.fax_number
            else:
                data['fax_number'] = ''
            
            facilities = user_profile.user.facilitymanger_set.all().annotate(id=F('facility__id'), name=F('facility__name')).values('id', 'name')
            for facility in facilities:
                data['facilities'].append(facility)
            
            return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: str) -> Response:
        user = user_repository.verify_account(uid=pk)
        serializer = UserInfoSerializer(data=request.data)
        is_reservation_active = reservation_connection_repository.check_reservation_active(city_code=user.partitioneduserprofile_set.get().region.city_code)
        if not serializer.is_valid():
            logger.error(f'UserInfoSerializer {request.data}')
            raise exceptions.ValidationException
        # caのユーザ情報を更新
        if user.partitioneduserprofile_set.get().account_type == 'general' and is_reservation_active:
            city_ca_repository.update_info(serializer.validated_data)
        #　施設管理者ユーザーの施設情報を更新
        if user.partitioneduserprofile_set.get().account_type == 'facility':
            user_repository.update_facility_manager(user, request.data['facilities'])
        # 本アプリのユーザ情報を更新
        user_repository.update_info(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: str) -> Response:
        user = user_repository.verify_account(uid=pk)
        is_reservation_active = reservation_connection_repository.check_reservation_active(city_code=user.partitioneduserprofile_set.get().region.city_code)
        updated_data = {
            'email': str(uuid.uuid4()) + '@deleted.com',
            'phone_number': '',
            'fax_number': '',
            'age': '',
            'age_range': '',
            'is_active': False,
            'kana_last_name': '',
            'kana_first_name':'',
            'last_name':'',
            'first_name':'',
            'user_type': '',
            'user_type_detail': '',
            'birthday':'',
            'postal_code_1':'',
            'postal_code_2':'',
            'address_prefecture':'',
            'address_city':'',
            'address_block':'',
            'disability_type': [],
            'disablity_grade':'',
            'disablity_prefecture': '',
            'disablity_number': '',
            'disability_category': [],
            'notification_tag': [],
            'note1': '',
            'note2': '',
            'note3': '',
            'expire_date1': '',
            'expire_date2': '',
            'expire_date3': '',
            'expire_date4': '',
            'expire_date5': '',
            'expire_date6': '',
            'expire_date7': '',
            'is_subscribe': False,
            'get_notification': False,
            'get_disaster_notification': False,
        }
        # caのユーザ情報を更新 
        if user.partitioneduserprofile_set.get().account_type == 'general' and is_reservation_active:
            city_ca_repository.update_info_for_delete(user.email)
        # 本アプリのユーザ情報をランダムな英数字で更新して削除とみなす
        user_repository.update_info_for_delete(user.email, updated_data)
        return Response(status=status.HTTP_200_OK)


class HelpCardView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTAppUserAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]


    def get(self, request: Request) -> Response:
        token = request.query_params.get('token')
        id = request.query_params.get('id')
        data = None
        is_finished = False
        user_profile = user_repository.get_profile(request.user)
        while(True):
            if not is_finished:
                data = user_repository.check_pdf_status_from_plus_focus(id=id, user_profile=user_profile)
                is_finished = data['is_finished']
            else:
                data = user_repository.get_pdf_from_plus_focus(token=token, user_profile=user_profile)
                break
        
        file_name = str(uuid.uuid4()) + ".pdf"
        user_repository.export_file_uplode_s3(file_name, data, user_profile.region.city_code)
        url = user_repository.create_download_url(file_name, user_profile.region)
        print(url)
        return HttpResponse(url, status=200)
    
        # response = HttpResponse(data, content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename={token}.pdf'
        # return response

        # return HttpResponse(pdf['Body'].read(), content_type=pdf['ContentType'])
    
    def post(self, request: Request) -> Response:
        user_profile = user_repository.get_profile(request.user)
        pdf_credentials = user_repository.create_pdf_in_plus_focus(user_profile=user_profile)
        return Response(data={'token': pdf_credentials['token'], 'id': pdf_credentials['id']}, status=status.HTTP_200_OK)