from django.contrib import admin

from django.forms import Textarea
from django.contrib.postgres.fields import ArrayField

from account.models.user import User
from account.models.user_profile import PartitionedUserProfile, FacilityManger

admin.site.register(User)

@admin.register(PartitionedUserProfile)
class PartitionedUserProfileAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    list_display = ['uid', 'region', 'email', 'account_type', 'created_at', 'updated_at']
    list_filter = ['region', 'account_type']


@admin.register(FacilityManger)
class FacilityMangerAdmin(admin.ModelAdmin):
    list_display = ['id', 'region', 'user', 'facility']
    list_filter = ['region']
    search_fields = ['user__email']