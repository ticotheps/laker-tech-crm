from rest_framework import serializers
from models import models


class AssetSerializer(serializers.ModelSerializer):
    
    class meta:
        model = Asset
        fields = '__all__'