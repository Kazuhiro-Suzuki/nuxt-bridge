from django.contrib import admin
from django.db import models

from .region import Region


class Email(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="region")
    notification_body = models.TextField(verbose_name='お知らせ', max_length=1500, null=True, blank=True)
    inquiry_body = models.TextField(verbose_name='お問い合わせ', max_length=1500, null=True, blank=True)
    signup_body = models.TextField(verbose_name='会員登録', max_length=1500, null=True, blank=True)
    reset_password_body = models.TextField(verbose_name='パスワードリセット', max_length=1500, null=True, blank=True)

    def __str__(self):
        return f'{self.region.name}[{self.region.city_code}]'
    
    class Meta:
        verbose_name_plural = '自治体別メールテキスト'


admin.site.register(Email)
