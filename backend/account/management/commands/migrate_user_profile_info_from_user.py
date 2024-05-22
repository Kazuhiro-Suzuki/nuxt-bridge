import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from account.models.user import User
from ...models.user_profile import PartitionedUserProfile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--city_code', required=True, type=int, help='add region to non-partitioned Django Model. Sample "131032" ')

    def handle(self, *args: Any, **options: Any):
        try:
            region = Region.objects.get(city_code=options['city_code'])
            users = User.objects.select_related()
            for user in users:
                if not user.region:
                    user.region = region

                if not PartitionedUserProfile.objects.filter(uid=user.uid):
                    partitioned_profile = PartitionedUserProfile.objects.create(
                        uid=user.uid,
                        region=user.region,
                        user=user,
                        phone_number=user.phone_number,
                        email=user.email,
                        fax_number=user.fax_number,
                        account_type=user.type,
                        is_subscribe=user.is_subscribe,
                        created_at=user.date_joined,
                    )
                    logger.info(partitioned_profile)
            objects_count = User.objects.bulk_update(users, ['region'])
            print(objects_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

