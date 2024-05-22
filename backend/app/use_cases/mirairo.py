import logging
from typing import Optional

from django.db import transaction

from account.models import User
from app.domain.mirairo_connect import view_models, api_client
from app.repositories import mirairo_repositories as repo
from utils import format_error_single_line
from utils.exceptions import Exception500

logger = logging.getLogger(__name__)


def get_mirairo_connect_initial_data(city_code: str, user: User) -> Optional[view_models.MirairoConnectViewModel]:
    if user.is_authenticated:
        city_code = user.partitioneduserprofile_set.get().region.city_code
    region_profile = repo.get_region_profile(city_code)
    if region_profile is None:
        return view_models.MirairoConnectViewModel(view_models.RegionProfile.default(), None)
    if user.is_authenticated:
        user_connection = repo.get_user_connection_view_model(user)
    else:
        user_connection = None
    return view_models.MirairoConnectViewModel(region_profile, user_connection)


def connect_to_mirairo_id(user: User, code: str):
    region = user.partitioneduserprofile_set.get().region
    context = region.mirairo_connect_profile.to_context()
    try:
        connection = api_client.request_connection(code, context.get_redirect_uri(region.city_code), context).unwrap()
        with transaction.atomic():
            repo.save_user_connection(user, connection).unwrap()
            certificates = api_client.request_certificates(connection, context).unwrap()
            for certificate in certificates:
                repo.save_user_certificate(user, certificate).unwrap()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise Exception500(str(e))


def disconnect_from_mirairo_id(user: User):
    region = user.partitioneduserprofile_set.get().region
    context = region.mirairo_connect_profile.to_context()
    try:
        connection = repo.get_user_connection(user)
        if connection is not None:
            api_client.revoke_connection(connection, context).unwrap()
        repo.delete_user_connection_and_certificates(user)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise Exception500(str(e))
