import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from app.models.mirairo import MirairoUserCertificate ,PartitionedMirairoUserCertificate


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--city_code', required=True, type=int, help='add region to non-partitioned Django Model. Sample "131032" ')

    def handle(self, *args: Any, **options: Any):
        try:
            region = Region.objects.get(city_code=options['city_code'])
            user_certificates = MirairoUserCertificate.objects.select_related()
            for user_certificate in user_certificates:
                user_certificate.region = region
                if not PartitionedMirairoUserCertificate.objects.filter(uid=user_certificate.uid):
                    partitioned_user_certificate = PartitionedMirairoUserCertificate.objects.create(
                        uid=user_certificate.uid,
                        region=user_certificate.region,
                        date_of_birth=user_certificate.date_of_birth,
                        certificate_type=user_certificate.certificate_type,
                        barrier_grade=user_certificate.barrier_grade,
                        barrier_variety=user_certificate.barrier_variety,
                        issued_by=user_certificate.issued_by,
                        myna_confirmed=user_certificate.myna_confirmed,
                        expiration_date=user_certificate.expiration_date,
                        date_of_issue=user_certificate.date_of_issue,
                        date_of_reissue=user_certificate.date_of_reissue,
                        created_by=user_certificate.created_by,
                        created_at=user_certificate.created_at,
                        updated_at=user_certificate.updated_at,
                        updated_by=user_certificate.updated_by
                    )
                    logger.info(partitioned_user_certificate)
            objects_count = MirairoUserCertificate.objects.bulk_update(user_certificates, ['region'])
            print(objects_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
