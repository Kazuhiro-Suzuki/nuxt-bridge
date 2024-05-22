import logging

from config import settings
from django.db import transaction
from django.db.models import Case, When, Value, IntegerField, Sum, Min, Q, F

from account.models import User
from account.models.user_profile import PartitionedUserProfile
from app.models.inquiry import Inquiry, PartitionedInquiry
from app.repositories import region_repositories
from app.repositories.ses_email_sender import Message, make_inquiry_body, SesEmailSender
from app.serializers.InquirySerializer import InquiryAdminUpdateSerializer
from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)


def get_object(user: User, city_code: str):
    try:
        inquiry_obj = PartitionedInquiry.objects.filter(created_to=user, region__city_code=city_code).order_by('-created_at')
        return inquiry_obj
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.INQUIRY)


def post_object(city_code: str, user: User, created_to: User, display_name: str, contents: str, category: str):
    try:
        region_object = region_repositories.get_object(city_code=city_code)
        message_type = 'inquiry' if user.partitioneduserprofile_set.get().account_type in ('general', 'facility') else 'reply'
        with transaction.atomic():
            return PartitionedInquiry.objects.create(
                display_name=display_name,
                region=region_object,
                message_type=message_type,
                category=category,
                contents=contents,
                created_to=created_to,
                created_by=user,
            )
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.INQUIRY)


def put_object(status: str, id):
    try:
        object = PartitionedInquiry.objects.get(id=id)
        with transaction.atomic():
            payload = {
                'status': status
            }
            serializer = InquiryAdminUpdateSerializer(object, payload)
            if not serializer.is_valid():
                raise exceptions.ValidationException
            return serializer.save()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.INQUIRY)


def get_all_objects(city_code: str):
    try:
        region_object = region_repositories.get_object(city_code=city_code)
        qs = PartitionedInquiry.objects.filter(
                region_id=region_object.id,
                message_type='inquiry'
            ).values('created_by__email').annotate(
            status_sum=Sum(
                Case(
                    When(status='pending', then=Value(1)),
                    When(status='inspecting', then=Value(1)),
                    When(status='completed', then=Value(0)),
                    # 値のフィールドは「IntegerField」にする
                    output_field=IntegerField())
            ),
            created_at=Min('created_at', filter=Q(status__in=['pending', 'inspecting'])),
            user_id=F('created_by')
        ).order_by('-status_sum', 'created_at')
        return qs
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.INQUIRY)


def send_email(created_to: User, city_code: str):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        message = Message()
        message.sender = settings.SENDER_EMAIL
        message.receiver = created_to.email
        message.subject = 'お問い合わせ配信の通知'
        message.body = make_inquiry_body(region_obj)
        sender = SesEmailSender()
        response_with_message = sender.send_email(message)
        if response_with_message.status != 'succeeded':
            raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)
