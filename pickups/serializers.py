from rest_framework import serializers
from pickups.models import Pickup


class PickupSerializer(serializers.ModelSerializer):
    # token = serializers.CharField(max_length=255, read_only=True)
    coordinates = serializers.SerializerMethodField(read_only=True)
    address = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    is_done = serializers.BooleanField(required=False)

    class Meta:
        model = Pickup
        fields = '__all__'
        # fields = ('id', 'update_time', 'name', 'phone_number', 'address', 'phone_number', 'description',
        #           'coordinates', 'is_active', 'is_done')
        # extra_kwargs = {'address': {'required': False}, 'is_active': {'required': False},
        #                 'phone_number': {'required': False}}

    def get_coordinates(self, obj):
        return [obj.longitude, obj.latitude]
