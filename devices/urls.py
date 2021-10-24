from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from devices import views

urlpatterns = [
    path('assets/api', views.AssetList.as_view()),
    path('assettags/api', views.AssetTagList.as_view()),
]