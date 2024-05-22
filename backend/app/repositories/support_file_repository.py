import logging

import json

import boto3

from account.models import User
from app.models.support_file import SupportFileImg

from config import settings
from utils import exceptions
from utils import format_error_single_line
from django.core.paginator import Paginator
import requests

from django.forms.models import model_to_dict

from app.models import SupportFileRegion, Region, SupportFileRepl

logger = logging.getLogger(__name__)


def __support_file(record):
    return{
        "id": record.id,
        "file": json.loads(json.dumps(record.file))
    }


def __support_file_repl(record):
    return{
        "id": record.id,
        "form_id": record.form_id,
        "repl": record.repl,
        "update_date": record.update_date
    }


def get_object(city_code: str):
    try:
        region_obj = Region.objects.get(city_code=city_code)
        res = SupportFileRegion.objects.filter(region_id=region_obj.id)
        return [__support_file(x) for x in res]
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def get_repl(user: User, form_id, page_cnt=10, page=1):
    try:
        res = SupportFileRepl.objects.filter(created_by=user.uid, form_id=form_id).order_by("-update_date")
        data_page = Paginator([__support_file_repl(x) for x in res], page_cnt)
        return {
            "data-page": data_page.get_page(page).object_list,
            "length": res.count(),
            "max-page": data_page.num_pages
        }
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def get_repl_id(user: User, reol_id):
    try:
        res = SupportFileRepl.objects.filter(created_by=user.uid, id=reol_id).first()
        return __support_file_repl(res)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def get_repl_form_output(support_file_id, user_id):
    try:
        res = SupportFileRegion.objects.get(id=support_file_id)
        res = SupportFileRepl.objects.filter(form_id__in=[x["formId"] for x in res.file["item"]], created_by=user_id)
        return [__support_file_repl(x) for x in res]
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def get_repl_file_output(file_id):
    try:
        res = SupportFileImg.objects.get(id=file_id)
        return __file_url(res.upload_file_key)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def set_repl(user: User, form_id, repl):
    try:
        res = SupportFileRepl.objects.create(created_by=user, form_id=form_id, repl=repl)
        return res.id
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def update_repl(id, repl, user: User):
    try:
        res = SupportFileRepl.objects.get(id=id, created_by=user.uid)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception403
    try:
        res.repl = repl
        res.save()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def upload_img(user, form_id, form_name, file):
    upload_file_key = f'support-file/{user.uid}/{form_id}/{form_name}/{file.name}'
    res = SupportFileImg.objects.create(created_by=user, upload_file_key=upload_file_key)

    #s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = boto3.resource('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    bucket = s3.Bucket(bucket_name)
    bucket.Object(upload_file_key).put(Body=file)
    return res.id


def download_img_url(user_id, id):
    try:
        res = SupportFileImg.objects.get(id=id, created_by=user_id)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception403
    return __file_url(res.upload_file_key)


def download_pdf(user, vuefile, support_file_id):
    json = {
        "url": '{}?support_file_id={}&user_id={}&vuefile={}'.format(settings.HTP_HTML_URL, support_file_id, user.uid, vuefile)
    }
    res = requests.post(settings.HTP_API_URL, json=json)
    return res.text


def __file_url(key):
    #s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = boto3.client('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    get_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=240,
        HttpMethod='GET')
    return get_url

