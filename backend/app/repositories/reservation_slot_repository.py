import logging
from datetime import datetime, timedelta
import requests
import json

from config import settings
from utils import exceptions
from utils.exceptions import ErrorMessage as ErrMsg

from app.repositories import reservation_connection_repository


logger = logging.getLogger(__name__)

def get_city_ca_access_info(city_code: str):
    try:
        connection = reservation_connection_repository.get_reservation_conection(city_code=city_code)
        city_ca_endpoint = connection.city_ca_endpoint
        city_ca_apikey = connection.city_ca_apikey
        return city_ca_endpoint, city_ca_apikey
    except Exception as e:
            logger.error(e)
            raise exceptions.Exception500(e)

def get_slot(city_code: str, slotId: list):
    try:
        city_ca_endpoint, city_ca_apikey = get_city_ca_access_info(city_code)
        url = f'https://{city_ca_endpoint}/slot?slot_id={",".join(slotId)}'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': city_ca_apikey
        }
        response = requests.get(url, headers=headers)
        logger.info(f'city ca /slot GET status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /slot GET error {json.loads(response.content)} slotId:{slotId}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_SLOT)


def find_slot(city_code: str, facility_id: str, menu_id: str, start_date: str, end_date: str):
    try:
        connection = reservation_connection_repository.get_reservation_conection(city_code=city_code)
        url = f'https://{connection.city_ca_endpoint}/findSlot'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        payload = {
            "cityCode": city_code,
        }
        if facility_id:
            payload["facilityId"] = facility_id
        if menu_id:
            payload["menuId"] = menu_id
        if start_date:
            payload["startDate"] = start_date
        if end_date:
            payload["endDate"] = end_date

        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'city ca /findSlot POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /findSlot POST error {payload} {json.loads(response.content)}')
            raise exceptions.Exception500(response)

        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_FIND_SLOT)


def find_slot_native(city_code: str, facility_id: str, start_date: str, end_date: str):
    try:
        connection = reservation_connection_repository.get_reservation_conection(city_code=city_code)
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        menu_url = f'https://{connection.city_ca_endpoint}/facility/{facility_id}/menu'
        menu_response = requests.get(menu_url, headers=headers)
        logger.info(f'city ca /facility/facility_id/menu GET status_code {menu_response.status_code}')
        if menu_response.status_code != 200:
            logger.error(f'city ca /facility/facility_id/menu GET error {json.loads(menu_response.content)} facility_id:{facility_id}')
            raise exceptions.Exception500
        if not json.loads(menu_response.content):
            # メニューが設定されていない場合
            logger.error(f'city ca /facility/facility_id/menu GET error {json.loads(menu_response.content)} facility_id:{facility_id}')
            return []
        menu_data = json.loads(menu_response.content)[0]    # メニューは一つしか使わない

        url = f'https://{connection.city_ca_endpoint}/findSlot'
        payload = {
            "facilityId": facility_id,
            "menuId": menu_data['id'],
            "startDate": start_date,
            "endDate": end_date,
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'city ca /findSlot POST ${response.status_code} ${payload} ${response.content}')
        if response.status_code != 200:
            logger.error(f'city ca /findSlot POST error ${payload} ${json.loads(response.content)}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_FIND_SLOT)


def find_customize_slot(city_code: str, facility_id: str, start_date: datetime, end_date: datetime):
    try:
        connection = reservation_connection_repository.get_reservation_conection(city_code=city_code)
        url = f'https://{connection.city_ca_endpoint}/findSlot'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }

        menu_url = f'https://{connection.city_ca_endpoint}/facility/{facility_id}/menu'
        menu_response = requests.get(menu_url, headers=headers)
        logger.info(f'city ca /facility/facility_id/menu GET status_code {menu_response.status_code}')
        if menu_response.status_code != 200:
            logger.error(f'city ca /facility/facility_id/menu GET error {json.loads(menu_response.content)} facility_id:{facility_id}')
            raise exceptions.Exception500
        if not json.loads(menu_response.content):
            # メニューが設定されていない場合
            logger.error(f'city ca /facility/facility_id/menu GET error {json.loads(menu_response.content)} facility_id:{facility_id}')
            return []
        menu_data = json.loads(menu_response.content)[0]    # メニューは一つしか使わない

        payload = {
            "cityCode": city_code,
            "facilityId": facility_id,
            "menuId": menu_data['id'],
            "startDate": start_date.strftime('%Y-%m-%d'),
            "endDate": end_date.strftime('%Y-%m-%d'),
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'city ca /findSlot POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /findSlot POST error {json.loads(response.content)} {payload}')
            raise exceptions.Exception500(response)
        return __convert_slot(json.loads(response.content), payload, start_date)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_FIND_SLOT)


def __convert_slot(slots, payload, start_date: datetime) -> dict:
    converted_slot = {'keys': [], 'divisions': {}}
    day_convert = {
        "Mon": "(月)",
        "Tue": "(火)",
        "Wed": "(水)",
        "Thu": "(木)",
        "Fri": "(金)",
        "Sat": "(土)",
        "Sun": "(日)"
    }
    #後で動的に変更必要
    for i in range(7):
        if(payload['cityCode'] == '142077'):
            days = (start_date + timedelta(days=i)).strftime('%a')
            converted_slot['keys'].append((start_date + timedelta(days=i)).strftime('%-m月%-d日') + day_convert[days])
        else:
            converted_slot['keys'].append((start_date + timedelta(days=i)).strftime('%-m月%-d日'))

    for slot in slots:
        if slot['cityCode'] != payload['cityCode']:
            continue
        if str(slot['facilityId']) != str(payload['facilityId']):
            continue
        #後で動的に変更必要
        if(payload['cityCode'] == '142077'):
            days = datetime.strptime(slot['date'], '%Y-%m-%d').strftime('%a')
            day = datetime.strptime(slot['date'], '%Y-%m-%d').strftime('%-m月%-d日') + day_convert[days]
        else:
            day = datetime.strptime(slot['date'], '%Y-%m-%d').strftime('%-m月%-d日')
            
        division = slot['division']
        if division not in converted_slot['divisions']:
            converted_slot['divisions'][division] = {}
        if day not in converted_slot['divisions'][division]:
            converted_slot['divisions'][division][day] = {
                'id': slot['id'],
                'mark': __convert_mark(slot['remainingNum'], payload['cityCode']),
                'openAt': slot['openAt'],
                'closeAt': slot['closeAt']
            }
    return converted_slot


def __convert_mark(remaining_number: int, city_code: str) -> str:
    mark = '〇'
    # TODO 環境変数化させる
    # TODO regionまたはfacility単位でDB保持にする必要があるかも

    #後で動的に変更必要
    if city_code == '142077':
        if remaining_number == 0:
            mark = '―'
        return mark
    
    if 0 < remaining_number < 3:
        mark = '△'
    elif remaining_number == 0:
        mark = '―'

    return mark
