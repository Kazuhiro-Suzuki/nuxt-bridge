import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from app.models.uploaded_file import NotificationFile


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--city_code', required=True, type=int, help='add region to non-partitioned Django Model. Sample "131032" ')

    def handle(self, *args: Any, **options: Any):
        try:
            region = Region.objects.get(city_code=options['city_code'])
            notification_files = NotificationFile.objects.select_related()
            for notification_file in notification_files:
                notification_file.region = region
                logger.info(notification_file)
            objects_count = NotificationFile.objects.bulk_update(notification_files, ['region'])
            print(objects_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))