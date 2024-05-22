import uuid

from django.contrib import admin
from django.db import models

from .region import Region


class ReservationConnection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='予約機能を有効にする')
    city_ca_endpoint = models.CharField(verbose_name='CityCaアクセスURL', max_length=256, null=True, blank=True)
    city_ca_apikey = models.CharField(verbose_name='CityCaアクセスAPIKey', max_length=255, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    messages = models.JSONField(blank=True,null=True,default=[])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.region.name}[{self.region.city_code}]'

    class Meta:
        verbose_name_plural = '予約システム連携情報'

admin.site.register(ReservationConnection)