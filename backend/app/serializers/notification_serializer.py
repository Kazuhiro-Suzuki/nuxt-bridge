from app.models.notification import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()
    city_code = serializers.CharField()
    is_disaster_info = serializers.BooleanField()
    active_since = serializers.DateTimeField()
    segment_birthday = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    segment_birthday_year = serializers.JSONField(required=False, allow_null=True, default=[])
    segment_birthday_month = serializers.JSONField(required=False, allow_null=True, default=[])
    segment_address_block = serializers.JSONField(required=False, allow_null=True, default=[])
    segment_age_range = serializers.JSONField(required=False, allow_null=True, default=[])
    segment_user_type = serializers.JSONField(required=False, allow_null=True, default=[])
    segment_disability_type = serializers.JSONField(required=False, allow_null=True, default=[])
    segment_notification_tag = serializers.JSONField(required=False, allow_null=True, default=[])
    segment_notification_category = serializers.JSONField(required=False, allow_null=True, default=[])



class NotificationModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subject = serializers.CharField()
    body = serializers.CharField()
    is_disaster_info = serializers.BooleanField()
    active_since = serializers.DateTimeField()

    class Meta:
        model = Notification
        fields = [
            'id',
             'subject', 
             'body', 
             'active_since',
             'is_disaster_info',
             'segment_birthday',
             'segment_birthday_year',
             'segment_birthday_month',
             'segment_address_block',
             'segment_age_range',
             'segment_user_type',
             'segment_disability_type',
             'segment_notification_tag',
             'segment_notification_category'
        ]
