from django.contrib import admin
from django.db import models

from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel

from account.models.user import User
from app.models.region import Region


class UserCityCa(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=512)  # city ca uuid

    class Meta:
        managed = True
        verbose_name_plural = 'CityCaユーザ'

    def __str__(self):
        return f'{self.user.email} / {self.uid}'


class PartitionedUserCityCa(PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']

    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=512)  # city ca uuid

    class Meta:
        managed = True
        verbose_name_plural = 'CityCaユーザ - パーティション'
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'region_id'], name='unique_for_user_city_ca')
        ]

    def __str__(self):
        return f'{self.user.email} / {self.uid}'

admin.site.register([UserCityCa, PartitionedUserCityCa])
