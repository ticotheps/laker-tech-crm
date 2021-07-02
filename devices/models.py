from django.db import models

class Device(models.Model):
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    imei_number = models.PositiveBigIntegerField()
    wlan_mac_address = models.CharField(max_length=50)
    lan_mac_address = models.CharField(max_length=50)
    replacement_fee = models.DecimalField(max_digits=6, decimal_places=2)
    
