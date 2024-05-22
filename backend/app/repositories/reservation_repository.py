import json
import logging
import requests

from config import settings
from utils import exceptions
from utils.exceptions import ErrorMessage as ErrMsg
from account.repositories import user_city_ca_repository, user_repository
from app.repositories import reservation_connection_repository

logger = logging.getLogger(__name__)



def get_reservation_connection(email: str = None, uid: str = None):
    if email:
        user_profile, user_ca = user_repository.get_object_with_ca(email=email)
    
    if uid:
        user_ca = user_city_ca_repository.get_object_by_uid(uid=uid)
        user_profile = user_repository.get_profile_with_uid(uid=uid)
        
    connection = reservation_connection_repository.get_reservation_conection(user_profile.region.city_code)
    
    return user_ca, connection


def create_reservation(email: str, temporaryReservationId: list, surveyResponse: list):
    try:
        user, connection = get_reservation_connection(email=email)
        url = f'https://{connection.city_ca_endpoint}/reservation'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        payload = {
            'customerUuid': user.uid,
            'temporaryReservationId': temporaryReservationId,
            'surveyResponse': surveyResponse,
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.error(f'city ca /reservation POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /reservation POST error ${json.loads(response.content)} ${payload}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_CREATE_RESERVE)


def cancel_reservation(email: str, reservation_id: str):
    try:
        user, connection = get_reservation_connection(email=email)
        url = f'https://{connection.city_ca_endpoint}/reservation/cancel'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        payload = {
            'customerUuid': user.uid,
            'reservationId': reservation_id,
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.error(f'city ca /reservation/cancel POST status_code ${response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /reservation/cancel POST error ${json.loads(response.content)} ${payload}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_CANCEL_RESERVE)


def get_reservation(uid: str, reservation_id: list):
    try:
        user, connection = get_reservation_connection(uid=uid)
        url = f'https://{connection.city_ca_endpoint}/customer/{user.uid}/findReservation'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        payload = {}
        if reservation_id:
            payload['id'] = reservation_id

        response = requests.post(url, headers=headers, json=payload)
        logger.error(f'city ca /customer/uid/findReservation POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /customer/uid/findReservation POST error ${json.loads(response.content)}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_RESERVE)
