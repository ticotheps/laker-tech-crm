from django.contrib import admin
from .models import (
    Asset,
    AssetTag,
    Borrower,
    BorrowerType,
    Building,
    City,
    # ContactInfo,
    Device,
    DeviceType,
    GraduationYear,
    School,
    # State
)

admin.site.register(Asset)
admin.site.register(AssetTag)
admin.site.register(Borrower)
admin.site.register(BorrowerType)
admin.site.register(Building)
admin.site.register(City)
# admin.site.register(ContactInfo)
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(GraduationYear)
admin.site.register(School)
# admin.site.register(State)