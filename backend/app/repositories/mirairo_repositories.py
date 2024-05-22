import logging
from typing import Optional

from account.models import User
from app.domain.mirairo_connect import data
from app.models import MirairoConnectRegionProfile
from app.models.mirairo import PartitionedMirairoUserConnection, PartitionedMirairoUserCertificate
from utils import format_error_single_line

from app.domain.mirairo_connect import view_models

logger = logging.getLogger(__name__)


def get_region_profile(city_code: str) -> Optional[view_models.RegionProfile]:
    try:
        record = MirairoConnectRegionProfile.objects.get(region__city_code=city_code)
        return view_models.RegionProfile(
            is_active=record.is_active,
            auth_url=record.auth_url,
            client_id=record.client_id,
            redirect_url_origin=record.redirect_url_origin,
        )
    except MirairoConnectRegionProfile.DoesNotExist:
        return None


def save_user_connection(user: User, connection: data.Connection) -> data.Result[None]:
    try:
        PartitionedMirairoUserConnection.objects.update_or_create(
            uid=user.uid,
            region=user.partitioneduserprofile_set.get().region,
            defaults={
                'access_token': connection.access_token,
                'token_type': connection.token_type,
                'expires_in': connection.expires_in,
                'refresh_token': connection.refresh_token,
            }
        )
        return data.Result.success(None)
    except Exception as e:
        logger.error(format_error_single_line(e))
        return data.Result.failure('failed to save user connection.')


def get_user_connection(user: User) -> Optional[data.Connection]:
    try:
        record = PartitionedMirairoUserConnection.objects.get(uid=user.uid)
        return data.Connection(
            access_token=record.access_token,
            token_type=record.token_type,
            expires_in=record.expires_in,
            refresh_token=record.refresh_token,
        )
    except PartitionedMirairoUserConnection.DoesNotExist:
        return None


def get_user_connection_view_model(user: User) -> Optional[view_models.UserConnection]:
    try:
        record = PartitionedMirairoUserConnection.objects.get(uid=user.uid)
        return view_models.UserConnection(
            connected_at=record.created_at
        )
    except PartitionedMirairoUserConnection.DoesNotExist:
        return None


def save_user_certificate(user: User, certificate: data.AnonymousCertificate) -> data.Result[None]:
    try:
        PartitionedMirairoUserCertificate.objects.update_or_create(
            uid=user.uid,
            region=user.partitioneduserprofile_set.get().region,
            defaults={
                'date_of_birth': certificate.date_of_birth,
                'certificate_type': certificate.certificate_type,
                'barrier_grade': certificate.barrier_grade,
                'barrier_variety': certificate.barrier_variety,
                'issued_by': certificate.issued_by,
                'myna_confirmed': certificate.myna_confirmed,
                'expiration_date': certificate.expiration_date,
                'date_of_issue': certificate.date_of_issue,
                'date_of_reissue': certificate.date_of_reissue,
            }
        )
        return data.Result.success(None)
    except Exception as e:
        logger.error(format_error_single_line(e))
        return data.Result.failure('failed to save user certificate.')


def delete_user_connection_and_certificates(user: User) -> data.Result[None]:
    try:
        PartitionedMirairoUserConnection.objects.filter(uid=user.uid).delete()
        PartitionedMirairoUserCertificate.objects.filter(uid=user.uid).delete()
        return data.Result.success(None)
    except Exception as e:
        logger.error(format_error_single_line(e))
        return data.Result.failure('failed to delete user connection or certificate.')
