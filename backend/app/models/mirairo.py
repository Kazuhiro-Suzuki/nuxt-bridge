from django.db import models

from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel

from . import Region
from .base_models import MutableSequenceModel
from ..domain.mirairo_connect.data import MirairoConnectContext


class MirairoConnectRegionProfile(MutableSequenceModel):
    region = models.OneToOneField(Region, related_name='mirairo_connect_profile', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False, verbose_name='ミライロID連携を有効にする')
    auth_url = models.CharField(max_length=255, verbose_name='ミライロ側の認証画面URL')
    client_id = models.CharField(max_length=255, verbose_name='OAuth2クライアントID')
    client_secret = models.CharField(max_length=255, verbose_name='OAuth2クライアントシークレット')
    redirect_url_origin = models.CharField(max_length=255, verbose_name='リダイレクトURLのオリジン')

    class Meta:
        verbose_name = verbose_name_plural = 'ミライロ連携自治体設定'

    def to_context(self) -> MirairoConnectContext:
        return MirairoConnectContext(
            api_base_url=self.auth_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_url_origin=self.redirect_url_origin,
        )


# account.User へ OneToOneField で参照しようとしたら循環依存が発生した
# 仕方ないので外部参照を使わないことにした
class MirairoUserConnection(MutableSequenceModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    uid = models.UUIDField(editable=False, primary_key=True)
    access_token = models.CharField(max_length=65535)
    token_type = models.CharField(max_length=255)
    expires_in = models.BigIntegerField(null=True, blank=True)
    refresh_token = models.CharField(max_length=65535, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'ユーザのミライロ連携トークン'


class PartitionedMirairoUserConnection(MutableSequenceModel, PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']

    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    uid = models.UUIDField(editable=False, primary_key=True)
    access_token = models.CharField(max_length=65535)
    token_type = models.CharField(max_length=255)
    expires_in = models.BigIntegerField(null=True, blank=True)
    refresh_token = models.CharField(max_length=65535, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'ユーザのミライロ連携トークン - パーティション'


# account.User へ OneToOneField で参照しようとしたら循環依存が発生した
# 仕方ないので外部参照を使わないことにした
class MirairoUserCertificate(MutableSequenceModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    uid = models.UUIDField(editable=False, primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True)
    certificate_type = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    barrier_grade = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    barrier_variety = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    issued_by = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    myna_confirmed = models.BooleanField()
    expiration_date = models.DateField(null=True, blank=True)
    date_of_issue = models.DateField(null=True, blank=True)
    date_of_reissue = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'ユーザの障害者手帳情報'


class PartitionedMirairoUserCertificate(MutableSequenceModel, PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']

    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    uid = models.UUIDField(editable=False, primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True)
    certificate_type = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    barrier_grade = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    barrier_variety = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    issued_by = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    myna_confirmed = models.BooleanField()
    expiration_date = models.DateField(null=True, blank=True)
    date_of_issue = models.DateField(null=True, blank=True)
    date_of_reissue = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'ユーザの障害者手帳情報 - パーティション'
