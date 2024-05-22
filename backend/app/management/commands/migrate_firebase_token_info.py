import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser

from app.models.region import Region
from app.models.firebase_token import FirebaseToken, PartitionedFirebaseToken


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        try:
            firebase_tokens = FirebaseToken.objects.select_related()
            for firebase_token in firebase_tokens:
                if not PartitionedFirebaseToken.objects.filter(id=firebase_token.id):
                    partitioned_firebase_token = PartitionedFirebaseToken.objects.create(
                        id=firebase_token.id,
                        region=firebase_token.region,
                        token=firebase_token.token,
                        created_at=firebase_token.created_at,
                    )
                    logger.info(partitioned_firebase_token)
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

