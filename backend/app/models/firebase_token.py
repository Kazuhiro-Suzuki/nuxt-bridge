from django.conf import settings
from django.contrib import admin
from django.db import models

from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel

from .region import Region


class FirebaseToken(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.region} / {self.token}'

    class Meta:
        verbose_name_plural = 'Firebaseトークン'


class PartitionedFirebaseToken(PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Firebaseトークン - パーティション'

admin.site.register([FirebaseToken])
