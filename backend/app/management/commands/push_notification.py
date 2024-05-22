import boto3
import logging
import datetime
import json
from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Q

from account.models.user_profile import PartitionedUserProfile
from app.models.notification import Notification, NotificationConnection
from app.models.firebase_token import PartitionedFirebaseToken
from app.repositories import notification_repositories

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'お知らせプッシュ通知のコマンド'
    client = boto3.client('sns', region_name=settings.AWS_REGION_NAME)
    message_content = dict

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)

    def _generate_endpoint(self, client, token, sns_arn):
        response = client.create_platform_endpoint(
            PlatformApplicationArn=sns_arn,
            Token=token,
            # CustomUserData='string',
            # Attributes={
            #     'string': 'string'
            # }
        )
        return response

    # def _push_notification(self, fcm_token):
    #     endpoint = self._generate_endpoint(client=self.client, token=fcm_token.token)
    #     try:
    #         message = {
    #             'GCM': json.dumps(self.message_content)
    #         }
    #         message_json = json.dumps(message)
    #         request = {
    #             'TargetArn': endpoint['EndpointArn'],
    #             'Message': message_json,
    #             'MessageStructure': 'json'
    #         }
    #         logger.info(f'push notification request: {request}')
    #         response = self.client.publish(**request)
    #         return response
    #     except Exception as e:
    #         logger.error(f'{e} push notification failed {endpoint}')

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        # コマンド実行した15分前から現在時刻までのお知らせをフィルタする
        start_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
        end_time = datetime.datetime.now()
        notifications = Notification.objects.filter(active_since__range=(start_time, end_time))
        logger.info(f'push notification: {notifications}')

        subscribers_for_normal_info = PartitionedUserProfile.objects.filter(get_notification=True).select_related('user')
        subscribers_for_disaster_info = PartitionedUserProfile.objects.filter(get_disaster_notification=True).select_related('user')
        
        for notification in notifications:
            notification_connection= NotificationConnection.objects.get(region=notification.region)
            sns_arn = notification_connection.sns_arn
            if notification.is_active:
                
                filter_fileds = Q()
                region_filed = Q(region=notification.region)
                if notification.segment_birthday:
                    filter_fileds = Q(birthday__contains=notification.segment_birthday)

                if notification.segment_birthday_year:
                    for year in notification.segment_birthday_year:
                        filter_fileds = filter_fileds | Q(birthday__contains=year)
                
                if notification.segment_birthday_month:
                    for month in notification.segment_birthday_month:
                        birthday_parts = month.split('-')
                        if len(birthday_parts) == 2:
                            segment_month = int(birthday_parts[1])
                            filter_fileds = filter_fileds | Q(birthday__contains=f'-{segment_month:02d}-')

                if notification.segment_age_range:
                    filter_fileds = filter_fileds| Q(age_range__in=notification.segment_age_range)
                
                if notification.segment_address_block:
                    filter_fileds = filter_fileds| Q(address_block__in=notification.segment_address_block)

                if notification.segment_user_type:
                    filter_fileds = filter_fileds| Q(user_type__in=notification.segment_user_type)

                if notification.segment_disability_type:
                    filter_fileds = filter_fileds| Q(disability_type__overlap=notification.segment_disability_type)
                
                if notification.segment_notification_tag:
                    filter_fileds = filter_fileds| Q(notification_tag__overlap=notification.segment_notification_tag)
                
                if not filter_fileds:
                    filter_fileds =  region_filed
                    logger.info(f'Region filtered:{filter_fileds}')
                    fcm_tokens = PartitionedFirebaseToken.objects.filter(filter_fileds)
                    notification_repositories.push_notification(self, fcm_tokens=fcm_tokens, notification=notification, sns_arn=sns_arn)
                else:
                    filter_fileds = filter_fileds & region_filed
                    logger.info(f'Multiple filtered:{filter_fileds}')
                    if not notification.is_disaster_info:
                        for subscriber_for_normal_info in subscribers_for_normal_info.filter(filter_fileds):
                            logger.info(f'subscriber_for_normal_info:{subscriber_for_normal_info}')
                            logger.info(f'user:{subscriber_for_normal_info.user}')
                            logger.info(f'region:{notification.region}')
                            logger.info(f'PartitionedFirebaseToken:{PartitionedFirebaseToken.objects.filter(user=subscriber_for_normal_info.user, region=notification.region)}')
                            fcm_tokens = PartitionedFirebaseToken.objects.filter(user=subscriber_for_normal_info.user, region=notification.region)
                            logger.info(f'fcm_tokens:{fcm_tokens}')
                            notification_repositories.push_notification(self, fcm_tokens=fcm_tokens, notification=notification, sns_arn=sns_arn)

                    if notification.is_disaster_info:
                        for subscriber_for_disaster_info in subscribers_for_disaster_info.filter(filter_fileds):
                            logger.info(f'subscriber_for_disaster_info:{subscriber_for_disaster_info}')
                            logger.info(f'user:{subscriber_for_disaster_info.user}')
                            logger.info(f'region:{notification.region}')
                            logger.info(f'PartitionedFirebaseToken:{PartitionedFirebaseToken.objects.filter(user=subscriber_for_disaster_info.user, region=notification.region)}')
                            fcm_tokens = PartitionedFirebaseToken.objects.filter(user=subscriber_for_disaster_info.user, region=notification.region)
                            logger.info(f'fcm_tokens:{fcm_tokens}')
                            notification_repositories.push_notification(self, fcm_tokens=fcm_tokens, notification=notification, sns_arn=sns_arn)




                # logger.info(f'push notification tokens: {fcm_tokens.count()}')

                # self.message_content = {
                #     'notification': {
                #         'title': notification.subject,
                #         'body': notification.body[:100],
                #         'sound': 'default',
                #     },
                #     'data': {
                #         'click_action': 'FLUTTER_NOTIFICATION_CLICK',
                #         'sound': 'default',
                #         'badge': 1,
                #     }
                # }
                
                # message = {
                #     'GCM': json.dumps(self.message_content)
                # }
                # message_json = json.dumps(message)
                # for fcm_token in fcm_tokens:
                #     endpoint = self._generate_endpoint(client=self.client, token=fcm_token.token, sns_arn=sns_arn)
                #     request = {
                #         'TargetArn': endpoint['EndpointArn'],
                #         'Message': message_json,
                #         'MessageStructure': 'json'
                #     }
                #     logger.info(f'push notification request: {request}')
                #     try:
                #         response = self.client.publish(**request)
                #         logger.info(f'success: {response}')
                #     except Exception as e:
                #         logger.info(f'error: {e} {endpoint}')
