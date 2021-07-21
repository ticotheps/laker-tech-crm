from django.contrib import admin
from .models import (
    Asset,
    AssetTag,
    Borrower,
    BorrowerType,
    Building,
    Device,
    DeviceType,
    GraduationYear,
    School
)

admin.site.register(Asset)
admin.site.register(AssetTag)
admin.site.register(Borrower)
admin.site.register(BorrowerType)
admin.site.register(Building)
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(GraduationYear)
admin.site.register(School)