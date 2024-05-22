from rest_framework import serializers
from app.models.facility import Facility

class FacilitySerializer(serializers.Serializer):
    city_code = serializers.CharField()
    postal_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    name = serializers.CharField()
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class FacilityNameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    city_code = serializers.CharField(required=False)


class FacilityListSerializer(serializers.ListSerializer):
    child = FacilityNameSerializer()


class FacilityModelSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    name = serializers.CharField()
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Facility
        fields = [
            'phone_number', 
            'name', 
            'address',
        ]

