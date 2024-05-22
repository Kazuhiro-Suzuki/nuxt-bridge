import logging
import datetime
from functools import reduce
from operator import or_
from typing import Any, Optional

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandParser

from account.models.user import User
from account.models.user_profile import PartitionedUserProfile

from app.models.notification import Notification
from app.repositories import notification_repositories

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'お知らせメール配信のコマンド'

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            # コマンド実行した15分前から現在時刻までのお知らせをフィルタする
            start_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
            end_time = datetime.datetime.now()
            notification_obj = Notification.objects.filter(active_since__range=(start_time, end_time))
            logger.info(f'send email notification: {notification_obj}')
       
            subscribers_for_normal_info = PartitionedUserProfile.objects.filter(is_subscribe=True).select_related('user')
            subscribers_for_disaster_info = PartitionedUserProfile.objects.filter(get_disaster_notification=True).select_related('user')
            
            for obj in notification_obj:
                if not obj.is_active:
                    continue

                filter_fileds = Q()
                region_filed = Q(region=obj.region)
                if obj.segment_birthday:
                    filter_fileds = Q(birthday__contains=obj.segment_birthday)
                
                if obj.segment_birthday_year:
                    for year in obj.segment_birthday_year:
                        filter_fileds = filter_fileds | Q(birthday__contains=year)
                
                if obj.segment_birthday_month:
                    for month in obj.segment_birthday_month:
                        birthday_parts = month.split('-')
                        if len(birthday_parts) == 2:
                            segment_month = int(birthday_parts[1])
                            filter_fileds = filter_fileds | Q(birthday__contains=f'-{segment_month:02d}-')
                
                if obj.segment_age_range:
                    filter_fileds = filter_fileds| Q(age_range__in=obj.segment_age_range)
                
                if obj.segment_address_block:
                    filter_fileds = filter_fileds| Q(address_block__in=obj.segment_address_block)

                if obj.segment_user_type:
                    filter_fileds = filter_fileds| Q(user_type__in=obj.segment_user_type)

                if obj.segment_disability_type:
                    filter_fileds = filter_fileds| Q(disability_type__overlap=obj.segment_disability_type)
                
                if obj.segment_notification_tag:
                    filter_fileds = filter_fileds| Q(notification_tag__overlap=obj.segment_notification_tag)
                
                if not filter_fileds:
                    filter_fileds =  region_filed
                else:
                    filter_fileds = filter_fileds & region_filed

                if not obj.is_disaster_info:
                    for subscriber_for_normal_info in subscribers_for_normal_info.filter(filter_fileds):
                        notification_repositories.send_email(user=subscriber_for_normal_info.user, city_code=obj.region.city_code, notification=obj)

                if obj.is_disaster_info:
                    for subscriber_for_disaster_info in subscribers_for_disaster_info.filter(filter_fileds):
                        notification_repositories.send_email(user=subscriber_for_disaster_info.user, city_code=obj.region.city_code, notification=obj)
        except Exception as e:
            logger.error(e)
