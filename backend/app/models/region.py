import boto3
import os

from config import settings
from datetime import datetime

from django.contrib import admin
from django.db import models

from .base_models import MutableSequenceModel


# def user_directory_path(instance, file_name):
#     basename = os.path.basename(file_name)
#     if isinstance(instance, Region):
#         return f'region-uploaded-files/{instance.city_code}/{basename}'


class Region(MutableSequenceModel):
    name = models.CharField(max_length=256)
    city_code = models.CharField(max_length=6, unique=True)
    active_since = models.DateField(verbose_name='利用開始日', null=True, blank=True)
    active_until = models.DateField(verbose_name='利用終了日', null=True, blank=True)
    email = models.EmailField(null=True, blank=True, verbose_name='代表メールアドレス')
    header_image = models.CharField(verbose_name='自治体別固定ヘッダー画像', max_length=256)
    favicon_image = models.CharField(verbose_name='自治体別ファビコン画像', max_length=256, null=True, blank=True)
    footer_pc_image = models.CharField(verbose_name='自治体別固定フッターPC画像', max_length=256, null=True, blank=True)
    footer_sp_image = models.CharField(verbose_name='自治体別固定フッターSP画像', max_length=256, null=True, blank=True)
    advertising_image1 = models.CharField(verbose_name='自治体別広告画像1', max_length=256, null=True, blank=True)
    advertising_image2 = models.CharField(verbose_name='自治体別広告画像2', max_length=256, null=True, blank=True)
    advertising_image3 = models.CharField(verbose_name='自治体別広告画像3', max_length=256, null=True, blank=True)
    advertising_image4 = models.CharField(verbose_name='自治体別広告画像4', max_length=256, null=True, blank=True)
    top_image = models.CharField(verbose_name='自治体別トップ画像', max_length=255, null=True, blank=True)
    header_text = models.CharField(max_length=128, default='障害者アプリ')
    phone_number = models.CharField(max_length=32, blank=True, null=True, verbose_name='電話番号')
    department = models.CharField(max_length=50, blank=True, null=True, verbose_name='担当部署')
    base_color = models.CharField(max_length=128, default='purple')
    light_color = models.CharField(max_length=128, default='purple')
    dark_color = models.CharField(max_length=128, default='purple')
    term_of_service = models.TextField(max_length=3000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self, now: datetime) -> bool:
        return self.active_since <= now <= self.active_until

    def __str__(self):
        return f'{self.name}[{self.city_code}]'

    class Meta:
        verbose_name_plural = '自治体'


admin.site.register(Region)
