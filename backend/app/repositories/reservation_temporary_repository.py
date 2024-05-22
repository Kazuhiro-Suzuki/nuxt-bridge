import logging
import requests
import json

from config import settings
from utils import exceptions
from utils.exceptions import ErrorMessage as ErrMsg
from account.repositories import user_city_ca_repository, user_repository
from app.repositories import reservation_connection_repository


logger = logging.getLogger(__name__)


def get_reservation_connection(email: str):
    user_profile = user_repository.get_profile(email=email)
    connection = reservation_connection_repository.get_reservation_conection(user_profile.region.city_code)
    
    return connection


def post_reservation_temporary(slot_id: list, email: str):
    try:
        connection = get_reservation_connection(email=email)
        url = f'https://{connection.city_ca_endpoint}/temporaryReservation'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        user_city_ca_obj = user_city_ca_repository.get_object_by_email(email=email)
        payload = {
            'customerUuid': user_city_ca_obj.uid,
            'slotId': slot_id
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'city ca /temporaryReservation POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /temporaryReservation POST error {response.content} {payload}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_RESERVE_TEMP_SLOT)


def cancel_reservation_temporary(email: str, temporary_reservation_id: list):
    try:
        connection = get_reservation_connection(email=email)
        url = f'https://{connection.city_ca_endpoint}/temporaryReservation/cancel'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        user_city_ca_obj = user_city_ca_repository.get_object_by_email(email=email)
        payload = {
            'customerUuid': user_city_ca_obj.uid,
            'temporaryReservationId': temporary_reservation_id,
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'city ca /temporaryReservation/cancel POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /temporaryReservation/cancel POST error {response.content} {payload}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_CANCEL_TEMP_SLOT)


def get_reservation_temporary(email: str):
    try:
        user_city_ca_obj = user_city_ca_repository.get_object_by_email(email=email)
        connection = get_reservation_connection(email=email)
        url = f'https://{connection.city_ca_endpoint}/customer/{user_city_ca_obj.uid}/temporaryReservation'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        response = requests.get(url, headers=headers)
        logger.info(f'city ca /customer/temporaryReservation GET status_code {response.status_code}')
        if response.status_code != 200:
            logger.info(f'city ca /customer/temporaryReservation GET error {response.content} uid:{user_city_ca_obj.uid}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_TEMP_SLOT)
