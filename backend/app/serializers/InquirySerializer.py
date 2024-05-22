from app.models.inquiry import Inquiry
from rest_framework import serializers


class InquirySerializer(serializers.Serializer):
    category = serializers.CharField()
    contents = serializers.CharField()


class InquiryAdminPostSerializer(serializers.Serializer):
    display_name = serializers.CharField()
    category = serializers.CharField()
    contents = serializers.CharField()


class InquiryAdminUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    class Meta:
        model = Inquiry
        fields = ['status']
