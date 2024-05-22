import os

from django.contrib import admin
from django.db import models
from config import settings

from app.models.region import Region
from app.models.notification import Notification
from .base_models import ImmutableUUIDModel
from utils.enum import Choosable


def user_directory_path(instance, file_name):
    basename = os.path.basename(file_name)
    if isinstance(instance, UploadedFile):
        return f'notification-uploaded-files/{basename}'

class ScopeType(Choosable):
    user_closed = 'ユーザー自身'
    public = '全体へ公開'

class UploadedFile(ImmutableUUIDModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    visible_scope = models.CharField(max_length=32, choices=ScopeType.choices(), default='user_closed')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='uploaded_by')

    def __str__(self):
        return f'{self.id} / {self.region} / {self.file_name}'

    class Meta:
        verbose_name_plural = 'ファイル'


class NotificationFile(ImmutableUUIDModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    upload_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'お知らせ内のファイル'

admin.site.register(NotificationFile)