from rest_framework import serializers
from account.models.user_profile import PartitionedUserProfile
from app.serializers.facility_serializer import FacilityListSerializer

class UserInfoSerializer(serializers.ModelSerializer):
    facilities = FacilityListSerializer(required=False)
    class Meta:
        model = PartitionedUserProfile
        fields = '__all__'

