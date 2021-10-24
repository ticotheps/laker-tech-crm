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

from devices.serializers import AssetSerializer
from rest_framework import generics

class AssetList(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
    
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