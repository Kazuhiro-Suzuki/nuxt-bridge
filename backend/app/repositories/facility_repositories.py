import logging
import json

from decimal import Decimal
from django.db import transaction
from django.forms.models import model_to_dict
from app.models.region import Region
from app.models.facility import Facility
from app.models.facility_category import FacilityCategory
from app.models.facility_list import FacilityDetail, FacilityImage, FacilityListRegionSetting
from app.repositories import region_repositories
from app.serializers.facility_serializer import FacilityModelSerializer
from utils import exceptions
from utils import format_error_single_line
from utils.exceptions import ErrorMessage as ErrMsg

logger = logging.getLogger(__name__)


def get_public_object(city_code: str, facility_type: str):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        categories = FacilityCategory.objects.select_related()
        facilities = Facility.objects.filter(region_id=region_obj.id, facility_type=facility_type).select_related('category')
        res = []
        for category in categories:
            dict= {
                'id': category.id,
                'name': category.name,
                'contents': category.contents,
                'facilityItems': []
            }
            for facility in facilities:
                if facility.category and (category == facility.category):
                    dict['facilityItems'].append(model_to_dict(facility))
            if dict['facilityItems']:
                res.append(dict)
        return res  
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FACILITY)


def get_all_public_object(city_code: str):
    region_obj = region_repositories.get_object(city_code=city_code)
    return Facility.objects.filter(region_id=region_obj.id)


def get_public_object_by_id(facility_id: str):
    try:
        return Facility.objects.get(id=facility_id)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FACILITY)


def get_public_object_by_ids(facility_ids: str):
    try:
        return Facility.objects.filter(id__in=facility_ids)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FACILITY)


def get_facility_list(city_code: str):
    region = region_repositories.get_object(city_code=city_code)
    facilities = Facility.objects.filter(region=region).order_by('id')
    facility_list = []    
    for facility in facilities:
        facility_data = {
            'city_code': region.city_code,
            'facility_id': facility.id,
            'facility_name': facility.name,
            'latitude': facility.latitude,
            'longitude': facility.longitude,
            'google_map': facility.google_map
        }        
        for detail in FacilityDetail.objects.filter(facility=facility):
            facility_data[detail.detail_id] = detail.value
        facility_data['image_list'] = [image.file_name for image in FacilityImage.objects.filter(facility=facility).order_by('display_order')]

        facility_list.append(facility_data)
    return facility_list


def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Object of type Decimal is not JSON serializable")


@transaction.atomic
def update_facility_list_cash(city_code: str):
    facility_list = get_facility_list(city_code=city_code)
    region = Region.objects.get(city_code=city_code)
    setting = FacilityListRegionSetting.objects.get(region=region)
    setting.list_cash = json.dumps(facility_list, default=decimal_to_float)
    setting.save()


def get_facility_list_region_setting(city_code: str):
    region = region_repositories.get_object(city_code=city_code)
    try:
        setting = FacilityListRegionSetting.objects.get(region=region)
        return {
            'citycode': city_code,
            'displaySetting': json.loads(setting.display_setting),
            'searchSetting': json.loads(setting.search_setting)
        }
    except Exception as e:
        return {}


def post_object(city_code: str, postal_code: str, phone_number: str,
                name: str, address: str):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        with transaction.atomic():
            facility = Facility.objects.create(
                region_id=region_obj.id,
                postal_code=postal_code,
                phone_number=phone_number,
                name=name,
                address=address,
                latitude=0,
                longitude=0
            )
            # FIXME: 施設一覧で施設を特定する際, idを使うよう修正
            facility.google_map = facility.id
            facility.save()
            return facility
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FACILITY)


def put_object(id: int, updated_data: dict):
    try:
        object = Facility.objects.get(id=id)
        with transaction.atomic():
            payload = {
                'phone_number': updated_data.get('phone_number'),
                'name': updated_data.get('name'),
                'address': updated_data.get('address'),
            }
            serializer = FacilityModelSerializer(object, payload)
            if not serializer.is_valid():
                raise exceptions.ValidationException
            return serializer.save()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FACILITY)
    

def delete_object(id: int):
    try:
        object = Facility.objects.get(id=id)
        with transaction.atomic():
            return object.delete()
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500(ErrMsg.FACILITY)
    

@transaction.atomic
def post_facility_json(city_code: str, facilities: str):
    print(city_code)
    region = Region.objects.get(city_code=city_code)
    for i, row in enumerate(facilities):
        if i == 0:
            detail_headers = list(row['details'].keys())    

        # 施設登録
        if city_code == "092134":     
            facility_id = row['ID']
        else:
            facility_id = row['事業所番号']

        f = Facility.objects.update_or_create(
            region=region,
            google_map=facility_id,
            defaults={
                'name': row['事業所名'].replace("¥n", " "),
                'latitude': row['map']['location']['lat'],
                'longitude': row['map']['location']['lng']
            })    
        # 施設画像
        for order, img_name in enumerate(row['images']):
            # TODO: リセットしてから更新するか確認
            FacilityImage.objects.update_or_create(
                facility=f[0],
                display_order=order,
                defaults={
                    'file_name': f'{city_code}/{img_name}'
                })
        
        for detail_id, header in enumerate(detail_headers):
            value = row['details'].get(header)   
            FacilityDetail.objects.update_or_create(
                facility=f[0],
                detail_id=detail_id,
                defaults={
                    'value': value
                })       
    update_facility_list_cash(city_code=city_code)             
    region_setting = []
    for detail_id, header in enumerate(detail_headers):
        region_setting.append({
            "detail_id": detail_id,
            "label": header,
            "display_id": detail_id,
            "sort_id": detail_id
        })

