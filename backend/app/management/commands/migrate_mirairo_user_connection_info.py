import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from app.models.mirairo import MirairoUserConnection, PartitionedMirairoUserConnection


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--city_code', required=True, type=int, help='add region to non-partitioned Django Model. Sample "131032" ')

    def handle(self, *args: Any, **options: Any):
        try:
            region = Region.objects.get(city_code=options['city_code'])
            user_connections = MirairoUserConnection.objects.select_related()
            for user_connection in user_connections:
                user_connection.region = region
                if not PartitionedMirairoUserConnection.objects.filter(uid=user_connection.uid):
                    partitioned_user_connection = PartitionedMirairoUserConnection.objects.create(
                        uid=user_connection.uid,
                        region=user_connection.region,
                        expires_in=user_connection.expires_in,
                        refresh_token=user_connection.refresh_token,
                        token_type=user_connection.token_type,
                        access_token=user_connection.access_token,
                        created_by=user_connection.created_by,
                        created_at=user_connection.created_at,
                        updated_at=user_connection.updated_at,
                        updated_by=user_connection.updated_by,
                    )
                    logger.info(partitioned_user_connection)
            objects_count = MirairoUserConnection.objects.bulk_update(user_connections, ['region'])
            print(objects_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))



