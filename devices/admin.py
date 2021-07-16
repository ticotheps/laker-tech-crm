from django.contrib import admin
from .models import Device, AssetTag, Borrower, School, DeviceType

admin.site.register(Device)
admin.site.register(AssetTag)
admin.site.register(Borrower)
admin.site.register(School)
admin.site.register(DeviceType)
