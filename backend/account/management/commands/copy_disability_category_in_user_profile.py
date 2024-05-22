import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from account.models.user import User
from ...models.user_profile import PartitionedUserProfile

logger = logging.getLogger(__name__)

# python manage.py copy_disability_category_in_user_profile --city_code 142077

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--city_code', required=True, type=int, help='add region to non-partitioned Django Model. Sample "131032" ')

    def handle(self, *args: Any, **options: Any):
        try:
            region = Region.objects.get(city_code=options['city_code'])
            user_profiles = PartitionedUserProfile.objects.filter(region=region)
            for user_profile in user_profiles:
                print(user_profile.disability_category)
                if user_profile.disability_category:
                    user_profile.list_disability_category = [user_profile.disability_category]
                logger.info(user_profile)
            objects_count = PartitionedUserProfile.objects.bulk_update(user_profiles, ['list_disability_category'])
            print(objects_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

