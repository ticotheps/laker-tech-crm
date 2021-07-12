from django.contrib import admin
from .models import Device, AssetTag, Borrower

admin.site.register(Device)
admin.site.register(AssetTag)
admin.site.register(Borrower)
