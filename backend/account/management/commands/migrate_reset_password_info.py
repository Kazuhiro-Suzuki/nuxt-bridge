import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from account.models.user import User
from ...models.reset_password import ResetPassword, PartitionedResetPassword

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--city_code', required=True, type=int, help='add region to non-partitioned Django Model. Sample "131032" ')

    def handle(self, *args: Any, **options: Any):
        try:
            region = Region.objects.get(city_code=options['city_code'])
            reset_passwords = ResetPassword.objects.select_related()
            for reset_password in reset_passwords:
                reset_password.region = region
                if not PartitionedResetPassword.objects.filter(uid=reset_password.uid):
                    partitioned_reset_password = PartitionedResetPassword.objects.create(
                        uid=reset_password.uid,
                        region=reset_password.region,
                        expiration_at=reset_password.expiration_at,
                        user=reset_password.user,
                        created_at=reset_password.created_at,
                    )
                    logger.info(partitioned_reset_password)
            objects_count = ResetPassword.objects.bulk_update(reset_passwords, ['region'])
            print(objects_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
