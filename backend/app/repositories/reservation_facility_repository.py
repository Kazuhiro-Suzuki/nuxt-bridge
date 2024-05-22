import json
import logging
import requests

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

def get_objects(city_code: str):
    try:
        connection = reservation_connection_repository.get_reservation_conection(city_code=city_code)
        url = f'https://{connection.city_ca_endpoint}/cityFacility/{city_code}'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': connection.city_ca_apikey
        }
        response = requests.get(url, headers=headers)
        logger.info(f'city ca /cityFacility GET status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /cityFacility GET error {response.content} citycode:{city_code}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_FACILITY)


def find_facility(city_code: str):
    try:
        city_ca_endpoint, city_ca_apikey = get_city_ca_access_info(city_code)
        url = f'https://{city_ca_endpoint}/findFacility'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': city_ca_apikey
        }
        payload = {

        }
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'city ca /findFacility POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /findFacility POST error {response.content} {payload}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_FACILITY)


def get_facility_detail(city_code: str, facility_id: str):
    try:
        city_ca_endpoint, city_ca_apikey = get_city_ca_access_info(city_code)
        url = f'https://{city_ca_endpoint}/facility/{facility_id}'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': city_ca_apikey
        }
        response = requests.get(url, headers=headers)
        logger.info(f'city ca /facility GET status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'city ca /facility GET error {response.content} facilityId:{facility_id}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_FACILITY)
