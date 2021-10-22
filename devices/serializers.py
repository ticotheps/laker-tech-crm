from rest_framework import serializers

from models import {
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
    State,
    Transaction
}


class AssetSerializer(serializers.ModelSerializer):
    
    class meta:
        model = Asset
        fields = '__all__'