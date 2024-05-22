from rest_framework import serializers


class ActivateAccountSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    city_code = serializers.CharField()
