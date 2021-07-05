from django.db import models

class Device(models.Model):
    DESKTOP     = 1
    NOTEBOOK    = 2
    TABLET      = 3
    HOTSPOT     = 4
    PROJECTOR   = 5
    IP_PHONE    = 6
    DOC_CAM     = 7
    HD_TV       = 8
    DRONE       = 9
    TRI_POD     = 10
    
    DEVICE_TYPE = (
        (DESKTOP, ('Desktop PC')),
        (NOTEBOOK, ('Notebook PC')),
        (TABLET, ('Tablet Device')),
        (HOTSPOT, ('WiFi Hotspot')),
        (PROJECTOR, ('Projector')),
        (IP_PHONE, ('IP Phone')),
        (DOC_CAM, ('Document Camera')),
        (HD_TV, ('High-Def TV')),
        (DRONE, ('Drone')),
        (TRI_POD, ('Camera Tri-Pod')),
    )
    
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE, default=NOTEBOOK)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, verbose_name='Serial Number')
    imei_number = models.PositiveBigIntegerField(verbose_name='IMEI Number')
    wlan_mac_address = models.CharField(max_length=17, verbose_name='WLAN MAC Address')
    lan_mac_address = models.CharField(max_length=17, verbose_name='LAN MAC Address')
    replacement_fee = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Replacement Fee', default=0.00)
    
    def __str__(self):
        return self.serial_number