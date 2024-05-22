from rest_framework import serializers


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
