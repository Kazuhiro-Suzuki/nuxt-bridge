import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from account.models.user import User
from ...models.user_city_ca import UserCityCa, PartitionedUserCityCa

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--city_code', required=True, type=int, help='add region to non-partitioned Django Model. Sample "131032" ')

    def handle(self, *args: Any, **options: Any):
        try:
            region = Region.objects.get(city_code=options['city_code'])
            user_city_cas = UserCityCa.objects.select_related()
            for user_city_ca in user_city_cas:
                user_city_ca.region = region
                if not PartitionedUserCityCa.objects.filter(uid=user_city_ca.uid):
                    partitioned_user_city_ca = PartitionedUserCityCa.objects.create(
                        id=user_city_ca.id,
                        region=user_city_ca.region,
                        uid=user_city_ca.uid,
                        user=user_city_ca.user,
                    )
                    logger.info(partitioned_user_city_ca)
            objects_count = UserCityCa.objects.bulk_update(user_city_cas, ['region'])
            print(objects_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
