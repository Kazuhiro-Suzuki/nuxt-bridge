from rest_framework import serializers


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    city_code = serializers.CharField()
