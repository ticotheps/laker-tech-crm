from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from devices import views

urlpatterns = [
    path('assets/', views.AssetList.as_view()),
    path('assettags/', views.AssetTagList.as_view()),
    path('borrowers/', views.BorrowerList.as_view()),
    path('borrowertypes/', views.BorrowerTypeList.as_view()),
    path('buildings/', views.BuildingList.as_view()),
    path('cities/', views.CityList.as_view()),
    path('contactinfoentries/', views.ContactInfoEntryList.as_view()),
    path('devices/', views.DeviceList.as_view()),
    path('devicecategories/', views.DeviceCategoryList.as_view()),
    path('devicemakers/', views.DeviceMakerList.as_view()),
    path('devicemodels/', views.DeviceModelList.as_view()),
    path('graduationyears/', views.GraduationYearList.as_view()),
    path('schools/', views.SchoolList.as_view()),
    path('transactions/', views.TransactionList.as_view()),
]