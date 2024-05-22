from rest_framework import serializers


class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    city_code = serializers.CharField()
