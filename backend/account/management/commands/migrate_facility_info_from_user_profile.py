import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from account.models.user import User
from ...models.user_profile import PartitionedUserProfile, FacilityManger

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any):
        try:
            user_profiles = PartitionedUserProfile.objects.filter(account_type='facility').select_related('facility')
            for user_profile in user_profiles:
                target_facility_managers = FacilityManger.objects.filter(user=user_profile.user, facility=user_profile.facility)
                if user_profile.facility and not target_facility_managers.exists():
                    facility_manager = FacilityManger.objects.create(
                        region=user_profile.region, 
                        user=user_profile.user, 
                        facility=user_profile.facility
                    )
                    logger.info(facility_manager)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
