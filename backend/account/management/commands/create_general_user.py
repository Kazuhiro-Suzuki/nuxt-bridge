import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from app.models.region import Region
from account.models.user import User
from account.models.user_profile import PartitionedUserProfile

from account.repositories import account_repository
from account.repositories import city_ca_repository, user_city_ca_repository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        ./manage.py create_general_user --email <email> --city_code <city_code>
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--email', dest='email', type=str)
        parser.add_argument('--city_code', dest='city_code', type=int)

    def handle(self, *args: Any, **options: Any):
        # password = account_repository.generate_password(8)
        password = 'Passw0rd'
        try:
            with transaction.atomic():
                region = Region.objects.get(city_code=options['city_code'])
                user = User.objects.create(
                    email=options['email'],
                    password=make_password(password),
                    is_active=1,
                    is_staff=0,
                    is_superuser=0,
                )
                user_profile = PartitionedUserProfile.objects.create(
                    uid=user.uid,
                    email=options['email'],
                    user=user,
                    region=region,
                    account_type='general',
                )
            # 本アプリのユーザ作成
            if user and user_profile:
                self.stdout.write(self.style.SUCCESS(f'app {user} created successfully. Password is {password}'))
            else:
                self.stdout.write(self.style.ERROR(f'{"app user failed."}'))

            # CityCaのユーザ作成
            user_ca = city_ca_repository.create_account_city_ca(user_profile=user_profile)
            if user_ca:
                self.stdout.write(self.style.SUCCESS(f'city ca {user_ca} created successfully.'))
            else:
                account_repository.delete_account(user=user, user_profile=user_profile)
                self.stdout.write(self.style.ERROR(f'{"city ca failed."}'))

            # 本アプリのユーザとCityCaのユーザを紐付け
            result = user_city_ca_repository.create_user_city_ca(user=user, uid=user_ca['uuid'], city_code=options['city_code'])
            if result:
                self.stdout.write(self.style.SUCCESS(f'user city ca {result} created successfully.'))
            else:
                account_repository.delete_account(user=user, user_profile=user_profile)
                self.stdout.write(self.style.ERROR(f'{"user city ca failed."}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
