from rest_framework import serializers


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_reconfirm = serializers.CharField()
    uid = serializers.CharField()
