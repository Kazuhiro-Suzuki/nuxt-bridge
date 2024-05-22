import logging

from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg

from app.repositories import region_repositories
from app.models.reservation import ReservationConnection


logger = logging.getLogger(__name__)


def get_reservation_conection(city_code: str):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        return ReservationConnection.objects.get(region=region_obj)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_RESERVE)

def check_reservation_active(city_code: str):
    region_obj = region_repositories.get_object(city_code=city_code)
    return ReservationConnection.objects.get(region=region_obj).is_active