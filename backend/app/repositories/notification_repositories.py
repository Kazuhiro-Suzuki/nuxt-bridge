import datetime
import json
import logging

from django.db import transaction
from django.db.models import Q

from account.models import User
from app.models.firebase_token import PartitionedFirebaseToken
from app.models.notification import Notification
from app.models.region import Region
from app.models.uploaded_file import NotificationFile
from app.serializers.notification_serializer import NotificationModelSerializer
from app.repositories import region_repositories
from app.repositories.ses_email_sender import Message, make_notification_body, SesEmailSender
from config import settings
from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)


def get_object_by_id(id: int, **kwargs):
    try:
        return Notification.objects.get(id=id)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_NOTIFICATION)

def get_object(city_code: str, **kwargs):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        return Notification.objects.filter(region_id=region_obj.id).order_by('-active_since')
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_NOTIFICATION)

def get_public_object(city_code: str):
    try:
        region_object = region_repositories.get_object(city_code=city_code)
        datetime_now = datetime.datetime.now()
        return Notification.objects.filter(region_id=region_object.id, active_since__lt=datetime_now).order_by('-active_since')
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_NOTIFICATION)

def get_public_object_per_user(user: User, city_code: str):
    try:
        region_object = region_repositories.get_object(city_code=city_code)
        datetime_now = datetime.datetime.now()

        notification_obj = Notification.objects.filter(region_id=region_object.id, active_since__lt=datetime_now).order_by('-active_since')

        if user.is_anonymous:
            notification_obj = notification_obj.filter(
                Q(segment_birthday__isnull=True) | Q(segment_birthday__exact=''),
                # Q(segment_address_block__isnull=True) | Q(segment_address_block__exact=''),
                segment_birthday_year__exact = [],
                segment_birthday_month__exact = [],
                segment_address_block__exact=[],
                segment_age_range__exact=[],
                segment_user_type__exact=[],
                segment_disability_type__exact=[],
                segment_notification_tag__exact=[],
                )
            return notification_obj
        
        if user.partitioneduserprofile_set.get().account_type == 'business':
            return notification_obj
        
        target_obj = []
        for obj in notification_obj:
            if not obj.segment_birthday and \
                not obj.segment_birthday_year and \
                not obj.segment_birthday_month and \
                not obj.segment_address_block and \
                not obj.segment_age_range and \
                not obj.segment_user_type and \
                not obj.segment_disability_type and \
                not obj.segment_notification_tag:
                target_obj.append(obj.id)
                continue

            if obj.segment_birthday and \
                obj.segment_birthday in (user.partitioneduserprofile_set.get().birthday or []):
                    target_obj.append(obj.id)
                    continue
            
            if obj.segment_birthday_year and \
                user.partitioneduserprofile_set.get().birthday:
                year = user.partitioneduserprofile_set.get().birthday.split('-')[0]
                if year in obj.segment_birthday_year:
                    target_obj.append(obj.id)
                    continue
            
            if obj.segment_birthday_month and \
                user.partitioneduserprofile_set.get().birthday:
                month = user.partitioneduserprofile_set.get().birthday.split('-')[1]
                if month in [segment_month.split('-')[1] for segment_month in obj.segment_birthday_month]:
                    target_obj.append(obj.id)
                    continue
            
            if obj.segment_age_range and \
                user.partitioneduserprofile_set.get().age_range in obj.segment_age_range:
                    target_obj.append(obj.id)
                    continue

            if obj.segment_address_block and \
                user.partitioneduserprofile_set.get().address_block in obj.segment_address_block:
                # obj.segment_address_block == user.partitioneduserprofile_set.get().address_block:
                    target_obj.append(obj.id)
                    continue

            if obj.segment_user_type and \
                user.partitioneduserprofile_set.get().user_type in obj.segment_user_type:
                    target_obj.append(obj.id)
                    continue

            if obj.segment_disability_type and \
                any(e in user.partitioneduserprofile_set.get().disability_type for e in obj.segment_disability_type):
                    target_obj.append(obj.id)
                    continue
            
            if obj.segment_notification_tag and \
                any(e in user.partitioneduserprofile_set.get().notification_tag for e in obj.segment_notification_tag):
                    target_obj.append(obj.id)
                    continue
        return notification_obj.filter(id__in=target_obj)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_NOTIFICATION)

def post_object(notification_data: dict):
    try:
        region_object = region_repositories.get_object(city_code=notification_data.get('city_code'))
        with transaction.atomic():
            return Notification.objects.create(
                subject=notification_data.get('subject'),
                body=notification_data.get('body'),
                is_active=True,
                is_disaster_info=notification_data.get('is_disaster_info'),
                segment_birthday=notification_data.get('segment_birthday'),
                segment_birthday_year=notification_data.get('segment_birthday_year'),
                segment_birthday_month=notification_data.get('segment_birthday_month'),
                segment_address_block=notification_data.get('segment_address_block'),
                segment_age_range=notification_data.get('segment_age_range'),
                segment_user_type=notification_data.get('segment_user_type'),
                segment_disability_type=notification_data.get('segment_disability_type'),
                segment_notification_tag=notification_data.get('segment_notification_tag'),
                segment_notification_category=notification_data.get('segment_notification_category'),
                active_since=notification_data.get('active_since'),
                region_id=region_object.id,
            )
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_POST_NOTIFICATION)


def put_object(updated_data: dict):
    try:
        object = Notification.objects.get(id=updated_data.get('id'))
        with transaction.atomic():
            payload = {
                'id': updated_data.get('id'),
                'subject': updated_data.get('subject'),
                'body': updated_data.get('body'),
                'is_disaster_info': updated_data.get('is_disaster_info'),
                'segment_birthday': updated_data.get('segment_birthday'),
                'segment_birthday_year': updated_data.get('segment_birthday_year'),
                'segment_birthday_month': updated_data.get('segment_birthday_month'),
                'segment_address_block': updated_data.get('segment_address_block'),
                'segment_age_range': updated_data.get('segment_age_range'),
                'segment_user_type': updated_data.get('segment_user_type'),
                'segment_disability_type':updated_data.get('segment_disability_type'),
                'segment_notification_tag': updated_data.get('segment_notification_tag'),
                'segment_notification_category': updated_data.get('segment_notification_category'),
                'active_since': updated_data.get('active_since'),
            }
            serializer = NotificationModelSerializer(object, payload)
            if not serializer.is_valid():
                raise exceptions.ValidationException
            return serializer.save()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_UPDATE_NOTIFICATION)


def delete_object(id: int):
    try:
        object = Notification.objects.get(id=id)
        with transaction.atomic():
            return object.delete()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_DELETE_NOTIFICATION)


def send_email(user: User, city_code: str, notification: Notification):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        message = Message()
        message.sender = settings.SENDER_EMAIL
        message.receiver = user.email
        if(city_code == '131237'):
            message.subject = '【お知らせ配信の通知】えどがわ障害者支援アプリ　ミライク -MIRAIKU-'
        else:
            message.subject = 'お知らせ配信の通知'
        
        message.body = make_notification_body(region_obj, notification)
        sender = SesEmailSender()
        response_with_message = sender.send_email(message)
        if response_with_message.status != 'succeeded':
            raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)


def create_notification_file(city_code: str, instance: Notification, files: list):
    try:
        region = Region.objects.get(city_code=city_code)
        with transaction.atomic():
            NotificationFile.objects.bulk_create([
               NotificationFile(region=region, upload_file=file, notification=instance) for file in files
            ])
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_POST_NOTIFICATION)


def get_file_ids_by_notification(id: str):
    try:
        notification_files = NotificationFile.objects.filter(notification=id)
        return [notification_file.upload_file.id for notification_file in notification_files]
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_NOTIFICATION)


def push_notification(self, fcm_tokens: PartitionedFirebaseToken, notification: Notification, sns_arn: str):
    logger.info(f'push notification tokens: {fcm_tokens.count()}')
    
    self.message_content = {
        'notification': {
            'title': notification.subject,
            'body': notification.body[:100],
            'sound': 'default',
        },
        'data': {
            'click_action': 'FLUTTER_NOTIFICATION_CLICK',
            'sound': 'default',
            'badge': 1,
        }
    }
    
    message = {
        'GCM': json.dumps(self.message_content)
    }
    message_json = json.dumps(message)
    for fcm_token in fcm_tokens:
        endpoint = self._generate_endpoint(client=self.client, token=fcm_token.token, sns_arn=sns_arn)
        request = {
            'TargetArn': endpoint['EndpointArn'],
            'Message': message_json,
            'MessageStructure': 'json'
        }
        logger.info(f'push notification request: {request}')
        try:
            response = self.client.publish(**request)
            logger.info(f'success: {response}')
        except Exception as e:
            logger.info(f'error: {e} {endpoint}')
