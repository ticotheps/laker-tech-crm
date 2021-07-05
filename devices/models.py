from django.db import models

class Device(models.Model):
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, verbose_name='Serial Number')
    imei_number = models.PositiveBigIntegerField(verbose_name='IMEI Number')
    wlan_mac_address = models.CharField(max_length=17, verbose_name='WLAN MAC Address')
    lan_mac_address = models.CharField(max_length=17, verbose_name='LAN MAC Address')
    replacement_fee = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Replacement Fee', default=0.00)
    
    def __str__(self):
        return self.name