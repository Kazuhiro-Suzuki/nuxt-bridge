from django.contrib import admin
from django.db import models

from . import Region


class PlusFocusConnection(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    plus_focus_endpoint = models.CharField(verbose_name='PlusFocusアクセスURL', max_length=255, null=True, blank=True)
    plus_focus_apikey = models.CharField(verbose_name='PlusFocusアクセスAPIKey', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = 'PlusFocus連携情報'

admin.site.register(PlusFocusConnection)