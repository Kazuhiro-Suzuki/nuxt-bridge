from rest_framework import serializers
from account.models.user_profile import PartitionedUserProfile
from app.serializers.facility_serializer import FacilityListSerializer

class SignUpSerializer(serializers.ModelSerializer):
    city_code = serializers.CharField()
    type = serializers.CharField()
    password = serializers.CharField()
    password_reconfirm = serializers.CharField()

    class Meta:
        model = PartitionedUserProfile
        fields = '__all__'

class SignUpFacilityUserSerializer(serializers.ModelSerializer):
    city_code = serializers.CharField()
    type = serializers.CharField()
    password = serializers.CharField()
    password_reconfirm = serializers.CharField()
    facilities = FacilityListSerializer()

    class Meta:
        model = PartitionedUserProfile
        fields = '__all__'