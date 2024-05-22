
from django.db import models
from django.contrib import admin

from .region import Region
from .facility_category import FacilityCategory
from utils.enum import Choosable


class FacilityType(Choosable):
    consultation_service = '相談窓口'
    disabled_facility = '障害者施設'


class Facility(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    address = models.CharField(max_length=2048, blank=True, null=True)
    facility_type = models.CharField(
        max_length=32, choices=FacilityType.choices(), default='disabled_facility'
    )
    category = models.ForeignKey(FacilityCategory, blank=True, null=True, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=8, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    fax_number = models.CharField(max_length=16, blank=True, null=True)
    google_map = models.CharField(max_length=2048, blank=True, null=True)
    contact = models.CharField(max_length=1024, blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    target = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # 施設一覧機能 関連
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.region} / {self.name}'

    class Meta:
        verbose_name_plural = '施設'
        indexes = [
            models.Index(fields=[
                'region',
                'facility_type',
                'category',
            ])
        ]
