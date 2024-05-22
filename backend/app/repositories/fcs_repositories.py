import json
import logging
import requests


from app.models import Facility
from config import settings
from utils import exceptions
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)

def post_fcs_object(facility: Facility):
    try:
        # region_obj = region_repositories.get_object(city_code=city_code)
        url = f'{settings.FCS_ENDPOINT}/{facility.region.city_code}/facility'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': f'{settings.FCS_APIKEY}'
        }
        payload = {
            "institution_name": f'{facility.id}',
            "name": facility.name,
            "region_id": f'{facility.region.city_code}'
        }
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f'fcs /cityFacility POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'fcs /cityFacility POST error {response.content} citycode:{facility.region.city_code}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_POST_FACILITY)
    


def put_fcs_object(facility: Facility):
    try:
        # region_obj = region_repositories.get_object(city_code=city_code)
        url = f'{settings.FCS_ENDPOINT}/{facility.region.city_code}/facility/{facility.id}'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': f'{settings.FCS_APIKEY}'
        }
        payload = {
            "institution_name": f'{facility.id}',
            "name": facility.name,
            "region_id": f'{facility.region.city_code}'
        }
        response = requests.put(url, headers=headers, json=payload)
        logger.info(f'fcs /cityFacility PUT status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'fcs /cityFacility PUT error {response.content} citycode:{facility.region.city_code}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_UPDATE_FACILITY)


def delete_fcs_object(facility: Facility):
    try:
        url = f'{settings.FCS_ENDPOINT}/{facility.region.city_code}/facility/{facility.id}'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': f'{settings.FCS_APIKEY}'
        }
        payload = {
            "institution_name": f'{facility.id}',
            "region_id": f'{facility.region.city_code}'
        }
        response = requests.delete(url, headers=headers, json=payload)
        logger.info(f'fcs /customer DELETE {json.loads(response.content)}')
        if response.status_code != 200:
            logger.error(f'fcs /cityFacility DELETE error {response.content} citycode:{facility.region.city_code}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_DELETE_FACILITY)