import logging

from app.models.region import Region
from app.models.email import Email
from utils import exceptions
from utils import format_error_single_line

logger = logging.getLogger(__name__)


def get_object(region: Region):
    try:
        return Email.objects.get(region=region)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500
