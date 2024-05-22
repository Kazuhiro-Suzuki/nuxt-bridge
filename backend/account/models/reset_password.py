import uuid

from django.contrib import admin
from django.db import models

from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel

from account.models.user import User
from app.models.region import Region


class ResetPassword(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    expiration_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        verbose_name_plural = 'パスワード変更'

    def __str__(self):
        return f'{self.user.email}'


class PartitionedResetPassword(PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']

    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    expiration_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        verbose_name_plural = 'パスワード変更 - パーティション'

    def __str__(self):
        return f'{self.region}/{self.uid}/{self.user.email}'

admin.site.register([ResetPassword, PartitionedResetPassword])
