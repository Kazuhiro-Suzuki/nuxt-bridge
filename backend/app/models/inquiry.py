from django.conf import settings
from django.contrib import admin
from django.db import models
from utils.enum import Choosable

from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel

from .base_models import ImmutableUUIDModel
from .region import Region


class MessageType(Choosable):
    inquiry = 'お問合せ'
    reply = '返信'


class CategoryType(Choosable):
    app = '本アプリの活用方法'
    notification = 'お知らせ内容'
    registration = '会員登録'
    mirairo = 'ミライロID'
    reservation = '短期入所施設予約'
    reserve_consult = 'オンライン相談予約'
    support_file = 'るぴなすノート'
    other = 'ご意見、その他'


class StatusType(Choosable):
    pending = '未対応'
    inspecting = '対応中'
    completed = '対応済み'


class Inquiry(ImmutableUUIDModel):

    class Meta:
        verbose_name_plural = 'お問合せ'
        indexes = [
            models.Index(fields=[
                'created_at',
            ]),
            models.Index(fields=[
                'created_at',
                'status',
            ])
        ]

    display_name = models.CharField(verbose_name='表示名', max_length=256, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    message_type = models.CharField(max_length=32, choices=MessageType.choices(), default='inquiry')
    category = models.CharField(max_length=32, choices=CategoryType.choices(), default='other')
    contents = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32, choices=StatusType.choices(), default='pending', db_index=True)
    created_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='inquiry_to')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='inquiry_by')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.region} / {self.display_name} / {self.created_at}'

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class PartitionedInquiry(ImmutableUUIDModel, PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']


    class Meta:
        verbose_name_plural = 'お問合せ - パーティション'
        indexes = [
            models.Index(fields=[
                'created_at',
            ]),
            models.Index(fields=[
                'created_at',
                'status',
            ])
        ]

    display_name = models.CharField(verbose_name='表示名', max_length=256, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    message_type = models.CharField(max_length=32, choices=MessageType.choices(), default='inquiry')
    category = models.CharField(max_length=32, choices=CategoryType.choices(), default='other')
    contents = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32, choices=StatusType.choices(), default='pending', db_index=True)
    created_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='contact_to')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='contact_by')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.region} / {self.display_name} / {self.created_at}'

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


admin.site.register([Inquiry])
