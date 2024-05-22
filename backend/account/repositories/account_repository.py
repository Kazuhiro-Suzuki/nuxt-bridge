import os
import datetime
import jwt
import logging
import string
import secrets
import re
import random
from typing import List

from django.db import transaction, IntegrityError
from django.db.models import CharField
from django.db.models.functions import Cast
from django.contrib.auth.hashers import make_password, check_password

from account.models.user import User
from account.models.user_profile import PartitionedUserProfile, FacilityManger
from account.models.reset_password import  PartitionedResetPassword
from app.models.region import Region
from app.models.facility import Facility
from app.repositories import region_repositories, facility_repositories
from app.repositories.ses_email_sender import Message, make_signup_body, make_reset_password_body, SesEmailSender
from account.repositories import user_repository
from config import settings
from utils import exceptions
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)
DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']


def login(is_mobile: bool, city_code: str, email: str, password: str):
    try:
        user = user_repository.get_object(email=email)
        if user.partitioneduserprofile_set.get().region.city_code != city_code:
            # logger.warning(f'citycode is different... {user}')
            raise exceptions.Exception401(ErrMsg.INCORRECT_REGION_USER)
        if not check_password(password, user.password):
            # logger.warning(f'password is incorrect... {user}')
            raise exceptions.Exception401(ErrMsg.INCORRECT_PASSWORD)
        if not user.is_active:
            # logger.warning(f'this account is not active... {user}')
            raise exceptions.Exception401(ErrMsg.INVALID_ACCOUNT)

        # facility_id = None
        # if user.partitioneduserprofile_set.get().facility:
        #     facility_id = user.partitioneduserprofile_set.get().facility.id

        facility_ids = []
        facility_managers = user.facilitymanger_set.all() 
        if facility_managers:
            for facility_manager in facility_managers:
                facility_ids.append(facility_manager.facility.id)

        user_info = user.partitioneduserprofile_set.values().annotate(
            uid=Cast('uid', output_field=CharField()),
            user_id=Cast('user_id', output_field=CharField()),
            created_at=Cast('created_at', output_field=CharField()),
            updated_at=Cast('updated_at', output_field=CharField()))
        for profile in user_info:
            user_info = {key: value for key, value in profile.items()}

        return generate_jwt(
                email=user.email, 
                type=user.partitioneduserprofile_set.get().account_type, 
                city_code=city_code, 
                facility_ids=facility_ids,
                user_info=user_info,
                is_mobile=is_mobile
            )
    except exceptions.Exception401 as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception401(e)


def login_without_password(city_code: str, email: str, from_path: str):
    try:
        if from_path != 'mirairo':
            raise exceptions.Exception401(ErrMsg.NOT_FROM_APP)
        user = user_repository.get_object(email=email)
        if not user.is_active:
            logger.error(f'this account is not active... {user}')
            raise exceptions.Exception401(ErrMsg.INVALID_ACCOUNT)
        
        # facility_id = None
        # if user.partitioneduserprofile_set.get().facility:
        #     facility_id = user.partitioneduserprofile_set.get().facility.id

        facility_ids = []
        facility_managers = user.facilitymanger_set.all() 
        if facility_managers:
            for facility_manager in facility_managers:
                facility_ids.append(facility_manager.facility.id)

        user_info = user.partitioneduserprofile_set.values().annotate(
            uid=Cast('uid', output_field=CharField()),
            user_id=Cast('user_id', output_field=CharField()),
            created_at=Cast('created_at', output_field=CharField()),
            updated_at=Cast('updated_at', output_field=CharField()))
        for profile in user_info:
            user_info = {key: value for key, value in profile.items()}
        
        return generate_jwt(
                email=user.email, 
                type=user.partitioneduserprofile_set.get().account_type, 
                city_code=city_code, 
                facility_ids=facility_ids,
                user_info=user_info
            )
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception401(e)


def generate_jwt(email: str, type: str, city_code: str, facility_ids: List[int], user_info: dict, is_mobile: bool = False):
    token_payload = {
        'email': email,
        'city_code': city_code,
        'type': type,
        'facility': facility_ids,
        'user_info': user_info,
        'exp': datetime.datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
    }
    token = jwt.encode(
        token_payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
    )

    refresh_token_payload = {
        'email': email,
        'city_code': city_code,
        'type': type,
        'facility': facility_ids,
        'user_info': user_info,
        'exp': datetime.datetime.utcnow() + settings.JWT_AUTH['REFRESH_JWT_EXPIRATION_DELTA']
    }

    if(city_code == '142077') and is_mobile:
        token_payload = {
            'email': email,
            'city_code': city_code,
            'type': type,
            'facility': facility_ids,
            'user_info': user_info,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
        }
        token = jwt.encode(
            token_payload,
            settings.SECRET_KEY,
            algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
        )
        refresh_token_payload = {
            'email': email,
            'city_code': city_code,
            'type': type,
            'facility': facility_ids,
            'user_info': user_info,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
        }
        print("Chigasaki current time:", datetime.datetime.utcnow())
        print("Chigasaki expire time:", datetime.datetime.utcnow() + datetime.timedelta(weeks=1))

    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
    )
    return (token, type, refresh_token)


def get_refresh_jwt(is_mobile: bool, refresh_token: str):
    user = decode_jwt(token=refresh_token)
    (token, _, refresh_token) = generate_jwt(
        email=user['email'],
        type=user['type'],
        facility_ids=user['facility'],
        user_info=user['user_info'],
        city_code=user['city_code'],
        is_mobile=is_mobile
    )
    return token, refresh_token


def get_token(headers: dict):
    if 'Authorization' not in headers:
        # logger.warning(f'token is None... {headers}')
        raise exceptions.Exception401(ErrMsg.INVALID_AUTH_INFO)
    bearer_token = headers['Authorization'].split(' ')
    if len(bearer_token) != 2 or bearer_token[0] != 'Bearer':
        # logger.warning(f'token is invalid... {headers}')
        raise exceptions.Exception401(ErrMsg.INVALID_AUTH_INFO)
    token = bearer_token[1]
    return token


def decode_jwt(token: str):
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.JWT_AUTH['JWT_ALGORITHM'],
        )
    except jwt.exceptions.DecodeError as e:
        logger.error(e)
        raise exceptions.Exception401(ErrMsg.INVALID_AUTH_INFO)
    except jwt.exceptions.ExpiredSignatureError as e:
        logger.error(e)
        raise exceptions.Exception401(ErrMsg.INVALID_AUTH_INFO)


def retrieve_user_from_token(token: str) -> User:
    payload = decode_jwt(token)
    return User.objects.get(email=payload['email'])


def generate_password(length=15):
    # chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # return ''.join(secrets.choice(chars) for _ in range(length))
    password = []
    for _ in range(6):
        password.append(secrets.choice(string.ascii_uppercase))
        password.append(secrets.choice(string.ascii_lowercase))
    for _ in range(3):
        password.append(secrets.choice(string.digits))
    random.shuffle(password)
    return "".join(password)
    
    


def create_account(user_data: dict):
    if user_data['password'] != user_data['password_reconfirm']:
        raise exceptions.Exception500(ErrMsg.PASSWORD_RECONFIRM)
    if not check_by_password_policy(user_data['password']):
        raise exceptions.Exception500(ErrMsg.PASSWORD_POLICY)
    # if not check_by_phone_policy(user_data['phone_number']):
    #     raise exceptions.Exception500(ErrMsg.ONLY_NUMBER_POLICY)
    try:
        region_obj = region_repositories.get_object(city_code=user_data['city_code'])
        with transaction.atomic():
            user, status_for_user = User.objects.get_or_create(
                email=user_data['email'],
                password=make_password(user_data['password']),
                is_active=0,
            )
            # facility = None
            # if user_data.get('facility'):
            #     facility=facility_repositories.get_public_object_by_id(user_data.get('facility').get('id'))
            

            if user_data.get('get_notification') is None:
                get_notification = True
            else:
                get_notification = user_data.get('get_notification')
            
            if user_data.get('get_disaster_notification') is None:
                get_disaster_notification = True
            else:
                get_disaster_notification = user_data.get('get_disaster_notification')

            
            # if user_data.get('get_notification'):
            #     get_notification = user_data.get('get_notification')
            # else:
            #     get_notification = True
            
            # if user_data.get('get_disaster_notification'):
            #     get_disaster_notification = user_data.get('get_disaster_notification')
            # else:
            #     get_disaster_notification = True
            
            user_profile, status_for_profile = PartitionedUserProfile.objects.get_or_create(
                uid=user.uid,
                email=user_data.get('email'),
                user=user,
                region=region_obj,
                phone_number=user_data.get('phone_number'),
                fax_number=user_data.get('fax_number'),
                kana_last_name=user_data.get('kana_last_name'),
                age=user_data.get('age'),
                age_range=user_data.get('age_range'),
                kana_first_name=user_data.get('kana_first_name'),
                user_type=user_data.get('user_type'),
                user_type_detail=user_data.get('user_type_detail'),
                account_type=user_data.get('type'),
                # facility=facility,
                last_name=user_data.get('last_name'),
                first_name=user_data.get('first_name'),
                birthday=user_data.get('birthday'),
                address_block=user_data.get('address_block'), 
                disability_type = user_data.get("disability_type"),
                disablity_grade = user_data.get("disablity_grade"),
                disablity_prefecture = user_data.get("disablity_prefecture"),
                disablity_number = user_data.get("disablity_number"),
                disability_category = user_data.get("disability_category"),
                notification_tag = user_data.get("notification_tag"),
                note1 = user_data.get("note1"),
                note2 = user_data.get("note2"),
                note3 = user_data.get("note3"),
                expire_date1 = user_data.get("expire_date1"),
                expire_date2 = user_data.get("expire_date2"),
                expire_date3 = user_data.get("expire_date3"),
                expire_date4 = user_data.get("expire_date4"),
                expire_date5 = user_data.get("expire_date5"),
                expire_date6 = user_data.get("expire_date6"),
                expire_date7 = user_data.get("expire_date7"),
                is_subscribe=1,
                get_notification=get_notification,
                get_disaster_notification=get_disaster_notification,
            )
            if status_for_user and status_for_profile:
                # send_create_account_email(user=user, city_code=city_code)
                return user, user_profile
    except IntegrityError as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.ALREADY_EXIST)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(e)


def send_create_account_email(user: User, city_code: str):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        message = Message()
        message.sender = settings.SENDER_EMAIL
        message.receiver = user.email
        message.subject = '会員登録のお知らせ'
        message.body = make_signup_body(region_obj, user.uid)
        sender = SesEmailSender()
        response_with_message = sender.send_email(message)
        if response_with_message.status != 'succeeded':
            raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)


def activate_account(uid: str, city_code: str):
    try:
        user = User.objects.get(uid=uid)
        if user.is_active:
            raise exceptions.Exception500(ErrMsg.ALREADY_VALID_ACCOUNT)
        with transaction.atomic():
            user.is_active = 1
            user.save()
            return user
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(e)


def send_reset_password_email(email: str, city_code: str):
    try:
        user = User.objects.get(email=email)
        region_obj = region_repositories.get_object(city_code=city_code)
        if not user.is_active:
            raise exceptions.Exception500(ErrMsg.INVALID_ACCOUNT)
        if user.partitioneduserprofile_set.get().region.city_code != city_code:
            raise exceptions.Exception500(ErrMsg.INCORRECT_REGION_USER)
        with transaction.atomic():
            reset_password = PartitionedResetPassword.objects.create(
                region=region_obj,
                user=user,
                expiration_at=datetime.datetime.now() + settings.RESET_PASSWORD_TIME
            )
            logger.info(f'reset password url is {settings.BASE_URL}/account/resetpassword?citycode={city_code}&uid={reset_password.uid}')
            message = Message()
            message.sender = settings.SENDER_EMAIL
            message.receiver = user.email
            message.subject = 'パスワードリセットの通知'
            message.body = make_reset_password_body(region_obj, reset_password.uid)
            sender = SesEmailSender()
            if DJANGO_SETTINGS_MODULE != 'config.settings_local':
                response_with_message = sender.send_email(message)
                if response_with_message.status != 'succeeded':
                    raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_SEND_EMAIL)


def update_password(password: str, password_reconfirm: str, uid: str):
    if password != password_reconfirm:
        raise exceptions.Exception500(ErrMsg.PASSWORD_RECONFIRM)
    if not check_by_password_policy(password):
        raise exceptions.Exception500(ErrMsg.PASSWORD_POLICY)
    try:
        obj = PartitionedResetPassword.objects.get(uid=uid)
        if obj.expiration_at < datetime.datetime.now():
            raise exceptions.Exception500(ErrMsg.EXPIRED_URL)
        user = User.objects.get(email=obj.user)
        with transaction.atomic():
            user.set_password(password)
            user.save()
            return user
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(e)


def check_by_password_policy(password):
    # 半角数字、大文字小文字の半角英字を含む8文字以上50文字以下
    pattern = r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,50}'
    return re.match(pattern, password)


def check_by_phone_policy(phone_number):
    pattern = r"^\d+$"
    return re.match(pattern, phone_number)


def delete_account(user: User, user_profile: PartitionedUserProfile):
    try:
        with transaction.atomic():
            return user.delete(), user_profile.delete()
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_EXEC_ACCOUNT)


def create_facility_manager(city_code: str, user: User, facilities: List[Facility]):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        facility_objs = facility_repositories.get_public_object_by_ids([facility['id'] for facility in facilities])
        with transaction.atomic():
            return FacilityManger.objects.bulk_create([
               FacilityManger(region=region_obj, user=user, facility=facility_obj) for facility_obj in facility_objs
            ])
    except Exception as e:
        logger.error(e)
        raise exceptions.Exception500(ErrMsg.FAILED_EXEC_ACCOUNT)