import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from app.models.inquiry import Inquiry, PartitionedInquiry


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        try:
            inquirys = Inquiry.objects.select_related()
            for inquiry in inquirys:
                if not PartitionedInquiry.objects.filter(id=inquiry.id):
                    partitioned_inquiry = PartitionedInquiry.objects.create(
                        id=inquiry.id,
                        region=inquiry.region,
                        display_name=inquiry.display_name,
                        message_type=inquiry.message_type,
                        category=inquiry.category,
                        contents=inquiry.contents,
                        status=inquiry.status,
                        updated_at=inquiry.updated_at,
                        created_at=inquiry.created_at,
                        created_by=inquiry.created_by,
                        created_to=inquiry.created_to,
                    )
                    logger.info(partitioned_inquiry)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
