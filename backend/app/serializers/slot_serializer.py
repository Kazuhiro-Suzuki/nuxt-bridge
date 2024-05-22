from rest_framework import serializers


class SlotSerializer(serializers.Serializer):
    city_code = serializers.CharField()
    facility_id = serializers.CharField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
