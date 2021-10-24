from rest_framework import serializers
from devices.models import (
    Asset,
    AssetTag,
    Borrower,
    BorrowerType,
    Building,
    City,
    ContactInfoEntry,
    Device,
    DeviceCategory,
    DeviceMaker,
    DeviceModel,
    GraduationYear,
    School,
    Transaction
)


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'