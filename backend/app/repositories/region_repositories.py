import logging

from app.models.region import Region
from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)


def get_object(city_code: str):
    try:
        return Region.objects.get(city_code=city_code)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_REGION)
