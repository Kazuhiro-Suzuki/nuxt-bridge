import logging

from django.forms.models import model_to_dict
from django.db.models import F


from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from app.serializers.facility_serializer import FacilitySerializer
from app.repositories import facility_repositories, fcs_repositories
from utils import exceptions
from utils.auth import JWTBusinessUserAuthentication

import json
from app import models
import re
# import googlemaps
# import datetime
from decimal import Decimal
import boto3
from config import settings
from django.db import transaction

logger = logging.getLogger(__name__)


class FacilityListView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        
        region = models.Region.objects.get(city_code=city_code)
        setting = models.FacilityListRegionSetting.objects.get(region=region)
        if not setting.list_cash:
            facility_repositories.update_facility_list_cash(city_code=city_code)

        return Response(data=json.loads(setting.list_cash), status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        data = request.data.get('facility')
        data = json.loads(data)
        # 施設更新
        region = models.Region.objects.get(city_code=city_code)

        f = models.Facility.objects.update_or_create(
            region=region,
            google_map=data['google_map'],
            defaults={
                'name': data['facility_name'],
                'latitude': Decimal(data['latitude']),
                'longitude': Decimal(data['longitude'])
            })    
            
        setting = models.FacilityListRegionSetting.objects.get(region=region)
        for item in json.loads(setting.display_setting):
            detail_id = str(item['detail_id'])
            if data.get(detail_id) is not None:
                models.FacilityDetail.objects.update_or_create(
                            facility=f[0],
                            detail_id=detail_id,
                            defaults={
                                'value': data[detail_id]
                            })         

        # 画像アップロード    
        for i in range(9):
            img = request.data.get(f'img{i}')
            if img:
                if type(img) == str:
                    image = models.FacilityImage.objects.get(
                        facility=f[0],
                        display_order=i
                    )  
                    image.file_name = img
                    image.save()

                else:
                    uploaded_file = request.FILES[f'img{i}']
                    # s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    #                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)                          
                    s3 = boto3.resource('s3')
                    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, key=f'facility-list/{city_code}/{uploaded_file.name}').put(Body=uploaded_file)                    
                    # s3.Object('lg-pwd-facility-list', key=f'facility-list/{city_code}/{uploaded_file.name}').put(Body=uploaded_file)        
        
                    models.FacilityImage.objects.update_or_create(
                                facility=f[0],
                                display_order=i,
                                defaults={
                                    'file_name': city_code + '/' + uploaded_file.name,
                                })       
            else:                
                image = models.FacilityImage.objects.filter(
                    facility=f[0],
                    display_order=i
                )       
                if image.exists():
                    image.delete()

        facility_repositories.update_facility_list_cash(city_code=city_code)
        return Response(status=status.HTTP_200_OK)    
    

class FacilityListRegionSetting(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        setting = facility_repositories.get_facility_list_region_setting(city_code=city_code)
        return Response(data=setting, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        setting = request.data.get('regionSetting')
        region = models.Region.objects.get(city_code=city_code)
        models.FacilityListRegionSetting.objects.update_or_create(
            region=region,
            defaults={'display_setting': json.dumps(setting.get('displaySetting')),
                      'search_setting': json.dumps(setting.get('searchSetting'))}           
        )

        return Response(status=status.HTTP_200_OK)        
    


class FacilityListFile(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = []

    # OPTIMIZE: 現時点では江戸川区→ミラボに施設ファイル連携の形でのみ使用
    def post(self, request) -> Response:
        if not (city_code := request.GET.get('city_code')):
            raise exceptions.ValidationException
        
        if city_code == "092134":
            facility_repositories.post_facility_json(
                city_code=city_code, facilities=request.data.get('jsonData'))    
        else:
            region = models.Region.objects.get(city_code=city_code)
            # TODO: 環境変数にする
            # google_maps = googlemaps.Client(key="")
            headers = []
            for i, row in enumerate(request.data.get('jsonData')):
                if i == 0:
                    headers = list(row.keys())      

                # 緯度・経度 設定
                # lat = None
                # lng = None
                # if google_maps and row['住所'].strip():
                #     result = google_maps.geocode(row['住所'])
                #     if result:
                #         address = result[0]["geometry"]["location"]
                #         lat = address['lat']
                #         lng = address['lng']

                # 施設登録
                lat = row['lat'] if row.get('lat') else None
                lng = row['lng'] if row.get('lng') else None            
                f = models.Facility.objects.update_or_create(
                    region=region,
                    google_map=row['事業者番号'],
                    defaults={
                        'name': row['事業所名'],
                        'latitude': lat,
                        'longitude': lng
                    })

                for detail_id, header in enumerate(headers):
                    value = row.get(header)   
                    if '事業所名' == header:
                        continue
                    if '画像' in header:
                        if value:
                            # 江戸川区の画像ファイル名が拡張子が2つ連続するためその前処理
                            # aaa.jpg → aaa.jpg.jpg
                            image_name = value
                            if city_code == '131237':
                                image_name = re.sub(r'\.([^.]+)$', r'.\1.\1', value)
                            models.FacilityImage.objects.update_or_create(
                                facility=f[0],
                                display_order=0,
                                defaults={
                                    'file_name': f'{city_code}/{image_name}'
                                })
                    else:
                        models.FacilityDetail.objects.update_or_create(
                            facility=f[0],
                            detail_id=detail_id,
                            defaults={
                                'value': value
                            })                                           

            region_setting = []
            for id, d in enumerate(headers):
                region_setting.append({
                    "detail_id": id,
                    "label": d,
                    "display_id": 0,
                    "sort_id": id
                })
            print(region_setting)

            # ローカルで緯度経度設定用
            # test = []
            # for i, l in enumerate(request.data.get('jsonData')):
            #     lat = ''
            #     lng = ''
            #     if google_maps and l['住所'].strip():
            #         print(l['住所'])
            #         result = google_maps.geocode(l['住所'])
            #         if result:
            #             address = result[0]["geometry"]["location"]
            #             lat = address['lat']
            #             lng = address['lng']
            #     l['lat'] = lat
            #     l['lng'] = lng
            #     test.append(l)        
            # return Response(data=test, status=status.HTTP_200_OK)            
        return Response(status=status.HTTP_200_OK)        

