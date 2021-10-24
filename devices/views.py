from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

from devices.serializers import (
    AssetSerializer,
    AssetTagSerializer,
    BorrowerSerializer,
    BorrowerTypeSerializer,
    BuildingSerializer,
    CitySerializer,
    ContactInfoEntrySerializer,
    DeviceSerializer,
    DeviceCategorySerializer,
    DeviceMakerSerializer,
    DeviceModelSerializer,
    GraduationYearSerializer,
    SchoolSerializer,
    TransactionSerializer
)
from rest_framework import generics

# Asset Views
class AssetList(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
# AssetTag Views
class AssetTagList(generics.ListCreateAPIView):
    queryset = AssetTag.objects.all()
    serializer_class = AssetTagSerializer 
class AssetTagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssetTag.objects.all()
    serializer_class = AssetTagSerializer

# Borrower Views
class BorrowerList(generics.ListCreateAPIView):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer 
class BorrowerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    
# BorrowerType Views
class BorrowerTypeList(generics.ListCreateAPIView):
    queryset = BorrowerType.objects.all()
    serializer_class = BorrowerTypeSerializer 
class BorrowerTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BorrowerType.objects.all()
    serializer_class = BorrowerTypeSerializer

# Building Views
class BuildingList(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer 
class BuildingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    
# City Views
class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer 
class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
# ContactInfoEntry Views
class ContactInfoEntryList(generics.ListCreateAPIView):
    queryset = ContactInfoEntry.objects.all()
    serializer_class = ContactInfoEntrySerializer 
class ContactInfoEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactInfoEntry.objects.all()
    serializer_class = ContactInfoEntrySerializer
    
# Device Views
class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer 
class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

# DeviceCategory Views
class DeviceCategoryList(generics.ListCreateAPIView):
    queryset = DeviceCategory.objects.all()
    serializer_class = DeviceCategorySerializer 
class DeviceCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceCategory.objects.all()
    serializer_class = DeviceCategorySerializer

# DeviceMaker Views
class DeviceMakerList(generics.ListCreateAPIView):
    queryset = DeviceMaker.objects.all()
    serializer_class = DeviceMakerSerializer 
class DeviceMakerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceMaker.objects.all()
    serializer_class = DeviceMakerSerializer
    
# DeviceModel Views
class DeviceModelList(generics.ListCreateAPIView):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer 
class DeviceModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer
    
# GraduationYear Views
class GraduationYearList(generics.ListCreateAPIView):
    queryset = GraduationYear.objects.all()
    serializer_class = GraduationYearSerializer 
class GraduationYearDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GraduationYear.objects.all()
    serializer_class = GraduationYearSerializer
    
# School Views
class SchoolList(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer 
class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    
# Transaction Views
class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer 
class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer    

# @api_view(['GET', 'POST'])
# def asset_list(request):
#     if request.method == 'GET':
#         assets = Asset.objects.all()
#         serializer = AssetSerializer(assets, many=True)

#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = AssetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)