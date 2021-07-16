from django.contrib import admin
from .models import Device, AssetTag, Borrower, School

admin.site.register(Device)
admin.site.register(AssetTag)
admin.site.register(Borrower)
admin.site.register(School)
