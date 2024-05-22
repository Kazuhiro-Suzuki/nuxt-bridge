from django.contrib import admin
from app.models import facility, faq ,firebase_token, inquiry ,mirairo, notification, uploaded_file, facility_list

# Register your models here.
admin.site.register(mirairo.MirairoConnectRegionProfile)


@admin.register(facility.Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_filter = ['region']
    search_fields = ['name']

@admin.register(facility_list.FacilityImage)
class FacilityImageAdmin(admin.ModelAdmin):
    list_display = ['file_name']

@admin.register(faq.FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_filter = ['region']

@admin.register(firebase_token.PartitionedFirebaseToken)
class PartitionedFirebaseTokenAdmin(admin.ModelAdmin):
    list_display = ['region', 'user','token', 'created_at', 'updated_at']
    list_filter = ['region']

@admin.register(inquiry.PartitionedInquiry)
class PartitionedInquiryAdmin(admin.ModelAdmin):
    list_filter = ['region']

@admin.register(mirairo.MirairoUserConnection)
class MirairoUserConnectionAdmin(admin.ModelAdmin):
    list_display = ['uid', 'expires_in', 'created_at', 'updated_at']

@admin.register(mirairo.PartitionedMirairoUserConnection)
class PartitionedMirairoUserConnectionAdmin(admin.ModelAdmin):
    list_display = ['uid', 'expires_in', 'created_at', 'updated_at']
    list_filter = ['region']

@admin.register(mirairo.MirairoUserCertificate)
class MirairoUserCertificateAdmin(admin.ModelAdmin):
    list_display = ['uid', 'certificate_type', 'created_at', 'updated_at']

@admin.register(mirairo.PartitionedMirairoUserCertificate)
class PartitionedMirairoUserCertificateAdmin(admin.ModelAdmin):
    list_display = ['uid', 'certificate_type', 'created_at', 'updated_at']
    list_filter = ['region']

@admin.register(notification.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter = ['region']

@admin.register(uploaded_file.UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'region', 'file_name', 'created_at']
    list_filter = ['region']
