import logging

from django.db import transaction

from account.models.user import User
from app.models.region import Region

from account.models.user_city_ca import PartitionedUserCityCa
from account.models.user_profile import PartitionedUserProfile

from utils import exceptions
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)


def create_user_city_ca(user: User, uid: str, city_code: str):
    try:
        region = Region.objects.get(city_code=city_code)
        with transaction.atomic():
            obj = PartitionedUserCityCa.objects.create(
                region=region,
                user=user,
                uid=uid,
            )
            return obj
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_CREATE_ACCOUNT)


def get_object(user: User):
    try:
        return PartitionedUserCityCa.objects.get(user=user)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500


def get_object_by_email(email: str):
    try:
        user = PartitionedUserProfile.objects.get(email=email).user
        return PartitionedUserCityCa.objects.get(user=user)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500


def get_object_by_uid(uid: str):
    try:
        user = PartitionedUserProfile.objects.get(uid=uid).user
        return PartitionedUserCityCa.objects.get(user=user)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500


def delete_object(uid: str):
    try:
        with transaction.atomic():
            object = PartitionedUserCityCa.objects.get(uid=uid)
            return object.delete()
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_EXEC_ACCOUNT)
