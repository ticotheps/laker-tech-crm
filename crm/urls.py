from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from devices import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^devices/', include('devices.urls'))
]
