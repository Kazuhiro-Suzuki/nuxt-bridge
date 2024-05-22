from django.contrib import admin
from django.db import models

from . import Region


class MicroServiceConnection(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    booklet_url = models.CharField(verbose_name='冊子アクセスURL', max_length=255, null=True, blank=True)
    survey_url = models.CharField(verbose_name='アンケートアクセスAPIKey', max_length=255, null=True, blank=True)
    congestion_url = models.CharField(verbose_name='混雑状況アクセスURL', max_length=255, null=True, blank=True)
    barrier_free_map_url = models.CharField(verbose_name='バリアフリーマップアクセスURL', max_length=255, null=True, blank=True)
    help_card_url = models.CharField(verbose_name='署名付ヘルプカードURL', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = 'マイクロサービスURL情報'

admin.site.register(MicroServiceConnection)