import logging
import requests
import json

from account.models.user import User
from app.models.region import Region
from account.repositories import user_repository
from app.repositories import reservation_connection_repository
from config import settings
from utils import exceptions
from utils.exceptions import ErrorMessage as ErrMsg

from account.models.user_city_ca import PartitionedUserCityCa
from account.models.user_profile import PartitionedUserProfile

logger = logging.getLogger(__name__)



def get_reservation_connection(uid: str = None, user_profile: PartitionedUserProfile = None):
    if uid:
        target_user_city_ca = PartitionedUserCityCa.objects.get(uid=uid)
        target_user= target_user_city_ca.user
        user_profile = user_repository.get_profile_with_uid(target_user.uid)
        
    connection = reservation_connection_repository.get_reservation_conection(user_profile.region.city_code)
    
    return connection


def create_account_city_ca(user_profile: PartitionedUserProfile):
    try:
        connection = get_reservation_connection(user_profile=user_profile)
        url = f'https://{connection.city_ca_endpoint}/customer'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        region_obj = Region.objects.get(id=user_profile.region_id)
        payload = {
            "cityCode": region_obj.city_code,
            "lastName": user_profile.last_name,
            "firstName": user_profile.first_name,
            "lastKana": user_profile.kana_last_name,
            "firstKana": user_profile.kana_first_name,
            "gender": 0,
            "birthday": user_profile.birthday or '2021-01-01',
            "age": "25",
            "postalCode": "",
            "address": "",
            "phoneNumber": user_profile.phone_number,
            "nickname": '',
            "email": user_profile.email
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'city ca /customer POST {json.loads(response.content)} {payload}')
        if response.status_code != 200:
            # account_repository.delete_account(user_profile)
            raise exceptions.Exception500(ErrMsg.FAILED_CREATE_ACCOUNT_B)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(e)


def update_info(updated_data: dict):
    try:
        '''
        1. caからユーザ情報をGET
        2. payloadを設定してPUT
        '''
        user_profile, user_ca = user_repository.get_object_with_ca(email=updated_data.get('email'))
        connection = get_reservation_connection(user_profile=user_profile)
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        url = f'https://{connection.city_ca_endpoint}/customer/{user_ca.uid}'

        get_response = requests.get(url, headers=headers)
        if get_response.status_code != 200:
            logger.error(f'city ca /customer GET error {json.loads(get_response.content)}')
            raise exceptions.Exception500(f'{""}')
        user_from_ca = json.loads(get_response.content)

        region_obj = Region.objects.get(id=user_profile.region_id)
        payload = {
            "cityCode": region_obj.city_code,
            "lastName": updated_data.get('last_name'),
            "firstName": updated_data.get('first_name'),
            "lastKana": updated_data.get('kana_last_name'),
            "firstKana": updated_data.get('kana_first_name'),
            "gender": user_from_ca['gender'],
            "birthday": updated_data.get('birthday') or '2021-01-01',
            "age": user_from_ca['age'],
            "postalCode": user_from_ca['postalCode'],
            "address": user_from_ca['address'],
            "phoneNumber": updated_data.get('phone_number'),
            "nickname": user_from_ca['nickname'],
            "email": user_from_ca['email']
        }
        put_response = requests.put(url, headers=headers, json=payload)
        if put_response.status_code != 200:
            logger.error(f'city ca /customer PUT error {json.loads(put_response.content)} {payload}')
            raise exceptions.Exception500(f'{""}')
        return json.loads(put_response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_UPDATE_USER_INFO)

def update_info_for_delete(email: str):
    try:
        '''
        1. payloadを設定してPUTすることで削除とみなす 
        '''
        user_profile, user_ca = user_repository.get_object_with_ca(email=email)
        connection = get_reservation_connection(user_profile=user_profile)
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        url = f'https://{connection.city_ca_endpoint}/customer/{user_ca.uid}'
        region_obj = Region.objects.get(id=user_profile.region_id)

        payload = {
            "cityCode": region_obj.city_code,
            "lastName": '',
            "firstName": '',
            "lastKana": '',
            "firstKana": '',
            "gender": 0,
            "birthday": '0001-01-01',
            "age": "0",
            "postalCode": '',
            "address": '',
            "phoneNumber": '',
            "nickname": '',
            "email": ''
        }
        put_response = requests.put(url, headers=headers, json=payload)
        if put_response.status_code != 200:
            logger.error(f'city ca /customer PUT for DELETE error {json.loads(put_response.content)} {payload}')
            raise exceptions.Exception500(f'{""}')
        return json.loads(put_response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_DELETE_USER_INFO)

def delete_account_city_ca(uuid: str):
    try:
        connection = get_reservation_connection(uid=uuid)
        url = f'https://{connection.city_ca_endpoint}/customer/{uuid}'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        response = requests.delete(url, headers=headers)
        logger.info(f'city ca /customer DELETE {json.loads(response.content)}')
        if response.status_code != 200:
            raise exceptions.Exception500(ErrMsg.FAILED_CREATE_ACCOUNT_B)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(e)
