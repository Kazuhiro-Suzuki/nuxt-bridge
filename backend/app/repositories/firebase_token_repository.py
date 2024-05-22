import logging

from django.db import transaction

from account.repositories import user_repository
from app.models.region import Region
from app.models.firebase_token import PartitionedFirebaseToken
from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)


def create_token_object(token: str, city_code: str):
    try:
        region = Region.objects.get(city_code=city_code)
        with transaction.atomic():
            return PartitionedFirebaseToken.objects.create(
                token=token,
                region=region,
            )
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.NOTIFICATION)

def create_or_update_token_object(token: str, city_code: str, uid: str):
    try:
        region = Region.objects.get(city_code=city_code)
        user = user_repository.get_object_with_uid(uid)
        print("create_or_update_token_object:", PartitionedFirebaseToken.objects.filter(token=token))
        with transaction.atomic():
            obj, created = PartitionedFirebaseToken.objects.update_or_create(
                token=token,
                region=region,
                defaults={'user': user}
            )
            return obj, created
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.NOTIFICATION)

def get_token_objects(city_code: str):
    try:
        region = Region.objects.get(city_code=city_code)
        return PartitionedFirebaseToken.objects.get(region=region)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.NOTIFICATION)


def verify_token(token: str):
    return PartitionedFirebaseToken.objects.filter(token=token).exists()
