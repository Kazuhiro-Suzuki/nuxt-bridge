from django.contrib import admin
from django.db import models
from .region import Region


class FAQ(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey('FAQCategory', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.region} / {self.question}'

    class Meta:
        verbose_name_plural = 'FAQ'


class FAQCategory(models.Model):
    name = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'FAQカテゴリ'


admin.site.register(FAQCategory)