from django.contrib import admin
from .models import Asset, AssetTag, Borrower, Device, DeviceType, School

admin.site.register(Asset)
admin.site.register(AssetTag)
admin.site.register(Borrower)
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(School)

