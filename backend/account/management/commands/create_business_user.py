import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from app.models.region import Region
from account.models.user import User
from account.models.user_profile import PartitionedUserProfile


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        ./manage.py create_business_user --email <email> --city_code <city_code>
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--email', dest='email', type=str)
        parser.add_argument('--city_code', dest='city_code', type=str)

    def handle(self, *args: Any, **options: Any):
        # password = account_repository.generate_password(8)
        common_password = 'Passw0rd'
        try:
            with transaction.atomic():
                region = Region.objects.get(city_code=options['city_code'])
                user = User.objects.create(
                    email=options['email'],
                    password=make_password(common_password),
                    is_active=1,
                    is_staff=0,
                    is_superuser=0,
                )
                user_profile = PartitionedUserProfile.objects.create(
                    uid=user.uid,
                    email=options['email'],
                    user=user,
                    region=region,
                    account_type='business',
                )
            if user and user_profile:
                self.stdout.write(self.style.SUCCESS(f'{user} created successfully. Password is {common_password}'))
            else:
                self.stdout.write(self.style.ERROR(f'{user} failed.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
