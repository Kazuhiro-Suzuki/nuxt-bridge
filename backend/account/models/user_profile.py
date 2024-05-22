import uuid
from utils.enum import Choosable

from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


from app.models.region import Region
from app.models.facility import Facility


class AccountType(Choosable):
    general = 'general_user'
    business = 'business_user'
    facility = 'facility_user'

class GenderType(Choosable):
    male = 'male'
    female = 'female'

        
class PartitionedUserProfile(PostgresPartitionedModel):
    
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']
    
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True, verbose_name='メールアドレス')
    phone_number = models.CharField(max_length=32, blank=True, null=True,verbose_name='電話番号')
    fax_number = models.CharField(max_length=32, blank=True, null=True, verbose_name='ファックス番号')
    gender =  models.CharField(max_length=32, blank=True, null=True, choices=GenderType.choices(), verbose_name='性別')
    age =  models.CharField(max_length=150, blank=True, null=True, verbose_name='年齢')
    age_range =  models.CharField(max_length=150, blank=True, null=True, verbose_name='年齢範囲')
    kana_last_name =  models.CharField(max_length=45, blank=True, null=True, verbose_name='姓（フリガナ）')
    kana_first_name =  models.CharField(max_length=45, blank=True, null=True, verbose_name='名（フリガナ）')
    last_name = models.CharField(max_length=45, blank=True, null=True,verbose_name='姓（漢字）')
    first_name = models.CharField(max_length=45, blank=True, null=True,verbose_name='名（漢字）')
    user_type = models.CharField(max_length=30, blank=True, null=True, verbose_name='障がい児者との関係')
    user_type_detail = models.TextField(null=True, blank=True, verbose_name='障がい児者との関係の詳細')
    account_type = models.CharField(max_length=16, choices=AccountType.choices(), default='general')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, blank=True, null=True, verbose_name='施設')
    birthday = models.CharField(max_length=10, blank=True, null=True, verbose_name='生年月日')
    postal_code_1 = models.CharField(max_length=3, blank=True, null=True, verbose_name='郵便番号-上3桁')
    postal_code_2 = models.CharField(max_length=4, blank=True, null=True, verbose_name='郵便番号-下4桁')
    address_prefecture = models.CharField(max_length=10, blank=True, null=True, verbose_name='都道府県')
    address_city = models.CharField(max_length=20, blank=True, null=True, verbose_name='市区町村')
    address_block = models.CharField(max_length=50, blank=True, null=True, verbose_name='番地')
    disability_type = ArrayField(models.CharField(max_length=50, blank=True, null=True), blank=True,null=True,default=list, verbose_name='障がい種別')
    disablity_grade =  models.CharField(max_length=20, blank=True, null=True, verbose_name='障がい等級')
    disablity_prefecture = models.CharField(max_length=20, blank=True, null=True, verbose_name='手帳の都道府県')
    disablity_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='手帳の号数')
    # disability_category = models.CharField(max_length=50, blank=True, null=True, verbose_name='障がいカテゴリー')
    disability_category = ArrayField(models.CharField(max_length=50, blank=True, null=True), blank=True,null=True,default=list, verbose_name='障がいカテゴリー')
    notification_tag = ArrayField(models.CharField(max_length=50, blank=True, null=True), blank=True,null=True,default=list, verbose_name='お知らせ配信のタグ')
    note1 = models.TextField(null=True, blank=True, verbose_name='備考1')
    note2 = models.TextField(null=True, blank=True, verbose_name='備考2')
    note3 = models.TextField(null=True, blank=True, verbose_name='備考3')
    expire_date1 = models.CharField(max_length=10, blank=True, null=True, verbose_name='有効期限1')
    expire_date2 = models.CharField(max_length=10, blank=True, null=True, verbose_name='有効期限2')
    expire_date3 = models.CharField(max_length=10, blank=True, null=True, verbose_name='有効期限3')
    expire_date4 = models.CharField(max_length=10, blank=True, null=True, verbose_name='有効期限4')
    expire_date5 = models.CharField(max_length=10, blank=True, null=True, verbose_name='有効期限5')
    expire_date6 = models.CharField(max_length=10, blank=True, null=True, verbose_name='有効期限6')
    expire_date7 = models.CharField(max_length=10, blank=True, null=True, verbose_name='有効期限7')
    is_subscribe = models.BooleanField(default=True, verbose_name='メール配信を有効にする')
    is_dangerous = models.BooleanField(default=False, verbose_name='要注意人物を有効にする')
    get_notification = models.BooleanField(default=True, verbose_name='通常のお知らせ通知を有効にする')
    get_disaster_notification = models.BooleanField(default=True, verbose_name='災害時のお知らせ通知を有効にする')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'ユーザプロファイル'
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'region_id'], name='unique_for_user_profile')
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        note1 = self._meta.get_field('note1')
        note2 = self._meta.get_field('note2')
        note3 = self._meta.get_field('note3')

        note1.verbose_name = '備考1'
        note2.verbose_name = '備考2'
        note3.verbose_name = '備考3'
        
        if self.region.city_code == '131237':
            note1.verbose_name = '障害・病気等の内容'
            note2.verbose_name = '知ってほしいこと'
            note3.verbose_name = '配慮してほしいこと'
        


class FacilityManger(PostgresPartitionedModel):
    
    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ['region_id']
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザ')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, verbose_name='施設')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '施設管理者'