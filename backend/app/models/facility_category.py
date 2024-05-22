
from django.db import models
from django.contrib import admin


class FacilityCategory(models.Model):
    name = models.CharField(max_length=1024)
    contents = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = '施設カテゴリ'


admin.site.register(FacilityCategory)
