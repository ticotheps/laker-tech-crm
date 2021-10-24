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

# Asset Serializer
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
        
# AssetTag Serializer
class AssetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTag
        fields = '__all__'
        
# Borrower Serializer
class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'
        
# BorrowerType Serializer
class BorrowerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowerType
        fields = '__all__'
        
# Building Serializer
class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'
        
# City Serializer
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        
# ContactInfoEntry Serializer
class ContactInfoEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfoEntry
        fields = '__all__'
        
# Device Serializer
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        
# DeviceCategory Serializer
class DeviceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCategory
        fields = '__all__'
        
# DeviceMaker Serializer
class DeviceMakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceMaker
        fields = '__all__'
        
# DeviceModel Serializer
class DeviceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = '__all__'
        
# GraduationYear Serializer
class GraduationYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationYear
        fields = '__all__'
        
# School Serializer
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        
# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'