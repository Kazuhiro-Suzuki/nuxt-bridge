import boto3

import logging
import os
import uuid

from config import settings
from django.core.files.base import ContentFile
from django.core.files.images import get_image_dimensions
from django.db import transaction
from django.shortcuts import get_object_or_404

from account.models import User
from app.models.uploaded_file import UploadedFile
from app.repositories import region_repositories

from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg


logger = logging.getLogger(__name__)

def get_object_from_s3(file_id: str, user: User):
    try:
        uploaded_file = get_object_or_404(UploadedFile, pk=uuid.UUID(file_id))
        if  uploaded_file.visible_scope == "user_closed" and uploaded_file.created_by != user:
            raise exceptions.Exception403
        # s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3 = boto3.resource('s3')
        file = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, key=uploaded_file.file.name).get()

        return file
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_FILE)

def save_object(city_code: str, files: list, user: User, visible_scope: str):
    try:
        response = {
            'uploaded_files': [],
            'error_file_names': []
        }
        content_type_dict = {
            '.jpeg': 'image/jpeg', '.jpg': 'image/jpeg', '.png': 'image/png'
        }
        region_object = region_repositories.get_object(city_code=city_code)
        for file in files:
            original_file_name = file.name
            root, ext = os.path.splitext(file.name)
            if ext.lower() not in content_type_dict.keys():
                response['error_file_names'].append(original_file_name)
            
            with transaction.atomic():
                width, height = get_image_dimensions(file)
                created_uploaded_file = UploadedFile.objects.create(
                            region=region_object,
                            file_name=file.name,
                            width=width,
                            height=height,
                            visible_scope=visible_scope,
                            created_by=user
                        )
                created_uploaded_file_id = created_uploaded_file.id
                file_bytes = file.read()
                upload_file_name = f'{created_uploaded_file_id}{ext}'
                created_uploaded_file.file.save(
                    upload_file_name,
                    ContentFile(file_bytes)
                )

            uploaded_file = {
                'id': created_uploaded_file_id,
                'original_name': original_file_name
            }
            response['uploaded_files'].append(uploaded_file)
            
        return response
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_POST_FILE)

def get_object(ids: list):
    try:
        uploaded_files = UploadedFile.objects.filter(id__in=ids)
        return uploaded_files
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_GET_FILE)


def delete_object(ids: list):
    try:
        uploaded_files = UploadedFile.objects.filter(id__in=ids)
        # s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        deleted_objects = bucket.delete_objects(Delete={"Objects": [{"Key": uploaded_file.file.name} for uploaded_file in uploaded_files]})
        with transaction.atomic():
            return uploaded_files.delete()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FAILED_DELETE_FILE)
