from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from devices import views

urlpatterns = [
    path('api', views.AssetList.as_view()),
]