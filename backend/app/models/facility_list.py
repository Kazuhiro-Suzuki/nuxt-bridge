from django.db import models
from django.contrib import admin
from .region import Region
from .facility import Facility


class FacilityListRegionSetting(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    display_setting = models.TextField(blank=True)
    search_setting = models.TextField(blank=True)
    list_cash = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)    

    class Meta:
        verbose_name_plural = '施設一覧の地域設定'


class FacilityDetail(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    detail_id = models.PositiveIntegerField()
    value = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)    

    class Meta:
        verbose_name_plural = '施設詳細'


class FacilityImage(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    file_name = models.TextField()
    display_order = models.PositiveIntegerField()    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)    

    class Meta:
        verbose_name_plural = '施設画像'        

admin.site.register(FacilityListRegionSetting)
admin.site.register(FacilityDetail)


