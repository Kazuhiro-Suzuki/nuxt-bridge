import boto3
import json
import logging
import requests

from django.db import transaction
from django.db.models import F

from account.models.user import User, Region
from account.models.user_city_ca import PartitionedUserCityCa
from account.models.user_profile import PartitionedUserProfile, FacilityManger
from app.models.facility import Facility
from app.models.plus_focus import PlusFocusConnection
from app.models.micro_service_connection import MicroServiceConnection
from app.repositories import facility_repositories, region_repositories
from app.repositories.ses_email_sender import Message, make_csv_download_body, SesEmailSender
from config import settings
from utils import exceptions, format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)


def get_object(email: str):
    try:
        return User.objects.get(email=email)
    except Exception as e:
        # logger.error(e)
        raise exceptions.Exception401(ErrMsg.NO_USER)


def get_profile(email: str):
    try:
        return PartitionedUserProfile.objects.get(email=email)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.NO_USER)


def get_object_with_ca(email: str):
    try:
        user_profile = PartitionedUserProfile.objects.filter(email=email).select_related('user').first()
        user_ca = PartitionedUserCityCa.objects.get(user_id=user_profile.user.uid)
        return user_profile, user_ca
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.NO_USER)


def get_profile_with_uid(uid):
    try:
        return PartitionedUserProfile.objects.get(uid=uid)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_USER_LIST)


def get_object_with_uid(uid):
    try:
        return User.objects.get(uid=uid)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_USER_LIST)


def get_object_list(city_code: str):
    try:
        region = Region.objects.get(city_code=city_code)
        return PartitionedUserProfile.objects.filter(region_id=region.id).select_related('user').order_by('-user__date_joined')
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_USER_LIST)

def get_object_list_per_account_type(city_code: str, account_type: str):
    try:
        region = Region.objects.get(city_code=city_code)
        return PartitionedUserProfile.objects.filter(region_id=region.id, account_type=account_type).select_related('user').order_by('-user__date_joined')
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_GET_USER_LIST)


def update_status(uid: str, is_active: bool, is_subscribe: bool, is_dangerous: bool):
    try:
        with transaction.atomic():
            user_profile = PartitionedUserProfile.objects.filter(uid=uid).select_related('user').first()
            user_profile.user.is_active = is_active
            user_profile.is_subscribe = is_subscribe
            user_profile.is_dangerous = is_dangerous
            user_profile.user.save()
            user_profile.save()
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_UPDATE_USER_INFO)


def update_info(updated_data: dict):
    try:
        with transaction.atomic():
            user_profile = PartitionedUserProfile.objects.get(email=updated_data.get('email'))
            user_profile.phone_number = updated_data.get('phone_number')
            user_profile.fax_number = updated_data.get('fax_number')
            user_profile.email = updated_data.get("email")
            user_profile.kana_last_name = updated_data.get("kana_last_name")
            user_profile.kana_first_name = updated_data.get("kana_first_name")
            user_profile.last_name = updated_data.get("last_name")
            user_profile.first_name = updated_data.get("first_name")
            user_profile.age = updated_data.get("age")
            user_profile.age_range=updated_data.get('age_range')
            user_profile.user_type = updated_data.get("user_type")
            user_profile.user_type_detail = updated_data.get("user_type_detail")
            user_profile.birthday = updated_data.get("birthday")
            user_profile.postal_code_1 = updated_data.get("postal_code_1")
            user_profile.postal_code_2 = updated_data.get("postal_code_2")
            user_profile.address_prefecture = updated_data.get("address_prefecture")
            user_profile.address_city = updated_data.get("address_city")
            user_profile.address_block = updated_data.get("address_block")
            user_profile.disability_type = updated_data.get("disability_type")
            user_profile.disablity_grade = updated_data.get("disablity_grade")
            user_profile.disablity_prefecture = updated_data.get("disablity_prefecture")
            user_profile.disablity_number = updated_data.get("disablity_number")
            user_profile.disability_category = updated_data.get("disability_category")
            user_profile.notification_tag = updated_data.get("notification_tag")
            user_profile.note1 = updated_data.get("note1")
            user_profile.note2 = updated_data.get("note2")
            user_profile.note3 = updated_data.get("note3")
            user_profile.expire_date1 = updated_data.get("expire_date1")
            user_profile.expire_date2 = updated_data.get("expire_date2")
            user_profile.expire_date3 = updated_data.get("expire_date3")
            user_profile.expire_date4 = updated_data.get("expire_date4")
            user_profile.expire_date5 = updated_data.get("expire_date5")
            user_profile.expire_date6 = updated_data.get("expire_date6")
            user_profile.expire_date7 = updated_data.get("expire_date7")
            user_profile.is_subscribe = updated_data.get('is_subscribe')
            user_profile.get_notification = updated_data.get("get_notification")
            user_profile.get_disaster_notification = updated_data.get("get_disaster_notification")
            user_profile.save()
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_UPDATE_USER_INFO)


def update_info_for_delete(old_email: str, updated_data: dict):
    try:
        with transaction.atomic():
            user_profile = PartitionedUserProfile.objects.filter(email=old_email).select_related('user').first()
            
            user_profile.email = updated_data["email"]
            user_profile.phone_number = updated_data["phone_number"]
            user_profile.fax_number = updated_data["fax_number"]
            user_profile.kana_last_name = updated_data["kana_last_name"]
            user_profile.kana_first_name = updated_data["kana_first_name"]
            user_profile.last_name = updated_data["last_name"]
            user_profile.first_name = updated_data["first_name"]
            user_profile.age = updated_data["age"]
            user_profile.age_range=updated_data['age_range']
            user_profile.birthday = updated_data["birthday"]
            user_profile.user_type = updated_data["user_type"]
            user_profile.user_type_detail = updated_data["user_type_detail"]
            user_profile.postal_code_1 = updated_data["postal_code_1"]
            user_profile.postal_code_2 = updated_data["postal_code_2"]
            user_profile.address_prefecture = updated_data["address_prefecture"]
            user_profile.address_city = updated_data["address_city"]
            user_profile.address_block = updated_data["address_block"]
            user_profile.disability_type = updated_data["disability_type"]
            user_profile.disablity_grade = updated_data["disablity_grade"]
            user_profile.disablity_prefecture = updated_data["disablity_prefecture"]
            user_profile.disablity_number = updated_data["disablity_number"]
            user_profile.disability_category = updated_data["disability_category"]
            user_profile.notification_tag = updated_data["notification_tag"]
            user_profile.note1 = updated_data["note1"]
            user_profile.note2 = updated_data["note2"]
            user_profile.note3 = updated_data["note3"]
            user_profile.expire_date1 = updated_data["expire_date1"]
            user_profile.expire_date2 = updated_data["expire_date2"]
            user_profile.expire_date3 = updated_data["expire_date3"]
            user_profile.expire_date4 = updated_data["expire_date4"]
            user_profile.expire_date5 = updated_data["expire_date5"]
            user_profile.expire_date6 = updated_data["expire_date6"]
            user_profile.expire_date7 = updated_data["expire_date7"]
            user_profile.is_subscribe = updated_data["is_subscribe"]
            user_profile.get_notification = updated_data["get_notification"]
            user_profile.get_disaster_notification = updated_data["get_disaster_notification"]
            
            user_profile.user.email = updated_data["email"]
            user_profile.user.is_active = updated_data["is_active"]

            user_profile.user.save()
            user_profile.save()
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_DELETE_USER_INFO)


def verify_account(uid: str):
    try:
        user = User.objects.get(uid=uid)
        if not user.is_active:
            raise exceptions.Exception500
        return user
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.INVALID_ACCOUNT)


def delete_facility_manager_by_user_and_facility(user: User, facility: Facility):
    try:
        object = FacilityManger.objects.filter(user=user, facility=facility)
        with transaction.atomic():
            return object.delete()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_DELETE_NOTIFICATION)  


def update_facility_manager(user: User, facilities: list):
    facility_managers = FacilityManger.objects.filter(user=user).select_related('facility')
    try:
        facility_managers = list(facility_managers.annotate(id=F('facility__id'), name=F('facility__name')).values('id', 'name'))
        for facility_manager in facility_managers:
            if not facility_manager in facilities:
                facility = facility_repositories.get_public_object_by_id(facility_manager['id'])
                delete_facility_manager_by_user_and_facility(user, facility)
        for facility in facilities:
            if not facility in facility_managers:
                facility = facility_repositories.get_public_object_by_id(facility['id'])
                facility_manager = FacilityManger.objects.create(
                    region=user.partitioneduserprofile_set.get().region, 
                    user=user, 
                    facility=facility
                )
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_UPDATE_USER_INFO)


def send_csv_download_email(informed_email: str, user: User, city_code: str):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        message = Message()
        message.sender = settings.SENDER_EMAIL
        message.receiver = user.email
        message.subject = 'ユーザー情報ダウンロードの通知'
        message.body = make_csv_download_body(informed_email, region_obj)
        sender = SesEmailSender()
        response_with_message = sender.send_email(message)
        if response_with_message.status != 'succeeded':
            raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)
    

def create_pdf_in_plus_focus(user_profile: PartitionedUserProfile):
    try:
        plus_focus = PlusFocusConnection.objects.get(region=user_profile.region)
        url = f'{plus_focus.plus_focus_endpoint}/render-pdf/a26c28b0-de3a-4c3b-b8a1-d5f54be1a76b/'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': plus_focus.plus_focus_apikey
        }
        payload = {
            "sheet_id": "a26c28b0-de3a-4c3b-b8a1-d5f54be1a76b",  
            "print": "True",
            "demanded_at": "",
            "item_inputs": {
                "776e9e1b-d51f-43e8-9dc5-3991050e04dc": [
                    {
                        "fragment_id": "91f21a19-98d1-4616-8fed-78d3389709d0",
                        "value": user_profile.kana_last_name + user_profile.kana_first_name
                    },
                    {
                        "fragment_id": "4724e6b6-1895-4840-b421-d386bfdab0f2",
                        "value": user_profile.last_name + user_profile.first_name
                    }
                ],
                "c97a6031-880e-40ef-92cf-3b16b4bf8a51": [
                    {
                        "fragment_id": "c45fb02d-d75f-4af0-ab4f-8d15a30e9b7b",
                        "value": user_profile.note3
                    }
                ],
                "6d53c3e7-3a52-49b0-92b5-77ca434436db": [
                    {
                        "fragment_id": "58918c8e-9c36-4dbb-993e-140277b8c02f",
                        "value": user_profile.phone_number
                    }
                ],
                "3390a90a-58b1-4972-9c40-9f7f796b5596": [
                    {
                        "fragment_id": "5a897cc1-dd32-4919-893e-3bd2ba56fcc4",
                        "value": user_profile.note1
                    }
                ],
                "a3b7cd7b-45b5-4319-a7a1-cc21a656348e": [
                    {
                        "fragment_id": "681b8b92-ddbe-4353-993e-b2396c8dfc6a",
                        "value": user_profile.note2
                    }
                ],
                "a05e57d8-7328-4c21-8d44-b45151f3ac29": [
                    {
                        "fragment_id": "eafd4e4c-b814-4af5-8d6d-8d3dfbaafb7f",
                        # "value": "目が不自由です。\n足が不自由です。\n発作があります。"
                        "value": "\n".join(user_profile.disability_category)
                    }
                ]
            }
        }
        response = requests.post(url, headers=headers, json=payload)

        logger.error(f'plus-focus POST status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'plus-focus POST error ${json.loads(response.content)} ${payload}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_CREATE_RESERVE)


def get_pdf_from_plus_focus(token: str, user_profile: PartitionedUserProfile):
    try:
        plus_focus = PlusFocusConnection.objects.get(region=user_profile.region)
        url = f'{plus_focus.plus_focus_endpoint}/get-rendered-pdf/{token}.pdf'
        headers = {
            'x-api-key': plus_focus.plus_focus_apikey
        }
        response = requests.get(url, headers=headers)

        logger.error(f'plus-focus Pdf GET status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'plus-focus Pdf GET error ${response.content}')
            raise exceptions.Exception500(response)
        return response.content
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_CREATE_RESERVE)
    

def check_pdf_status_from_plus_focus(id: str, user_profile: PartitionedUserProfile):
    try:
        plus_focus = PlusFocusConnection.objects.get(region=user_profile.region)
        url = f'{plus_focus.plus_focus_endpoint}/api/jobs/{id}/'
        headers = {
            'x-api-key': plus_focus.plus_focus_apikey
        }
        response = requests.get(url, headers=headers)

        logger.error(f'plus-focus Check GET status_code {response.status_code}')
        if response.status_code != 200:
            logger.error(f'plus-focus Check GET error ${json.loads(response.content)}')
            raise exceptions.Exception500(response)
        return json.loads(response.content)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_CREATE_RESERVE)

def export_file_uplode_s3(file_name, file, city_code):
    # s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = boto3.resource('s3')
    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, key=f'user-info/{city_code}/{file_name}').put(Body=file)
       
def create_download_url(file_name: str, region: Region):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from botocore.signers import CloudFrontSigner

    qs = MicroServiceConnection.objects.get(region=region)

    def rsa_signer(message):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name="ap-northeast-1"
        )
        get_secret_value_response = client.get_secret_value(
            SecretId="cloudfrontSignedUrlsPrivateKey"
        )
        cloudfront_pk_text = get_secret_value_response['SecretString']
        cloudfront_pk_bytes = str.encode(cloudfront_pk_text, encoding='ascii')

        private_key = serialization.load_pem_private_key(
            cloudfront_pk_bytes,
            password=None,
            backend=default_backend()
        )
        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

    cloudfront_signer = CloudFrontSigner('K3AUDPS58JC829', rsa_signer)

    from datetime import datetime, timedelta
    expire_date = datetime.utcnow() + timedelta(minutes=15)
    # 署名付きURLの発行
    return cloudfront_signer.generate_presigned_url(f'{qs.help_card_url}/user-info/{region.city_code}/' + file_name, date_less_than=expire_date)