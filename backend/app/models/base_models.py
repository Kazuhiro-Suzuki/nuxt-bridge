import uuid

from django.db import models


class ImmutableSequenceModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64)

    objects = models.Manager()

    class Meta:
        abstract = True


class ImmutableUUIDModel(ImmutableSequenceModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64)

    class Meta:
        abstract = True


class MutableSequenceModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class MutableUUIDModel(MutableSequenceModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
