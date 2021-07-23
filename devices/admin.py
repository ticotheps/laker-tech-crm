from django.contrib import admin
from .models import (
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
)

admin.site.register(Asset, ordering=['asset_tag'])
admin.site.register(AssetTag, ordering=['tag_id'])
admin.site.register(Borrower, ordering=['first_name'])
admin.site.register(BorrowerType, ordering=['name'])
admin.site.register(Building, ordering=['name'])
admin.site.register(City, ordering=['name'])
admin.site.register(ContactInfoEntry, ordering=['address_1'])
admin.site.register(Device, ordering=['device_maker'])
admin.site.register(DeviceCategory, ordering=['name'])
admin.site.register(DeviceMaker, ordering=['name'])
admin.site.register(DeviceModel, ordering=['name'])
admin.site.register(GraduationYear, ordering=['year'])
admin.site.register(School, ordering=['name'])
admin.site.register(State, ordering=['name'])
admin.site.register(Transaction, ordering=['transaction_date'])