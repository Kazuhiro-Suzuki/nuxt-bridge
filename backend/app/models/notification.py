import uuid

from django.db import models
from django.contrib import admin

from .region import Region
from .base_models import MutableSequenceModel


class Notification(MutableSequenceModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    subject = models.CharField(max_length=256)
    body = models.TextField(max_length=2048)
    active_since = models.DateTimeField(verbose_name='掲載開始日時')
    is_active = models.BooleanField(default=False)
    is_disaster_info = models.BooleanField(default=False, verbose_name='災害情報を有効にする')
    segment_birthday = models.CharField(max_length=20, null=True, blank=True, verbose_name='セグメント配信-生年月日')
    segment_birthday_year = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-誕生年')
    segment_birthday_month = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-誕生月')
    segment_address_block = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-住所')
    segment_age_range = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-年齢範囲')
    segment_user_type = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-障がい児者との関係')
    segment_disability_type = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-障がい種別')
    segment_notification_tag = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-お知らせ配信のタグ')
    segment_notification_category = models.JSONField(blank=True,null=True,default=list, verbose_name='セグメント配信-お知らせ配信のカテゴリ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.region} / {self.subject}'

    class Meta:
        verbose_name_plural = 'お知らせ'


class  NotificationConnection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    server_key = models.CharField(verbose_name='Cloud Messaging API Key', max_length=500, null=True, blank=True)
    sns_arn = models.CharField(verbose_name='プッシュ通知プラットフォーム ARN', max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.region.name}[{self.region.city_code}]'

    class Meta:
        verbose_name_plural = 'FCM連携情報'

admin.site.register(NotificationConnection)

