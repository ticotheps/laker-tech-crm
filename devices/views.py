from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

from serializers import AssetSerializer

@api_view(['GET', 'POST'])
def asset_list(request):
    if request.method == 'GET':
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_BAD_REQUEST)