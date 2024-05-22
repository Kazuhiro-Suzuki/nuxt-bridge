import uuid

from django.conf import settings
from django.contrib import admin
from django.db import models

from .region import Region


def default_file():
    return {}


class SupportFileRegion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    file = models.JSONField(blank=True, null=True, default=[])

    def __str__(self):
        return f'{self.region.name}[{self.region.city_code}]'

    class Meta:
        verbose_name_plural = 'サポートファイル設定'


admin.site.register(SupportFileRegion)


class SupportFileRepl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    form_id = models.UUIDField(default=uuid.uuid4)
    repl = models.JSONField(blank=True, null=True, default=[])
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = 'サポートファイル回答'


admin.site.register(SupportFileRepl)


class SupportFileImg(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    upload_file_key = models.CharField(max_length=511)
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = 'サポートファイル画像ファイル'


admin.site.register(SupportFileImg)
