from django.db import models

class Device(models.Model):
    # Choices for 'device_type' field.
    SELECT      = 1
    DESKTOP     = 2
    NOTEBOOK    = 3
    TABLET      = 4
    HOTSPOT     = 5
    PROJECTOR   = 6
    IP_PHONE    = 7
    DOC_CAM     = 8
    HD_TV       = 9
    SWIVL       = 10
    DRONE       = 11
    TRI_POD     = 12
    DEVICE_TYPE = (
        (SELECT, ('Select Device Type')),
        (DESKTOP, ('Desktop PC')),
        (NOTEBOOK, ('Notebook PC')),
        (TABLET, ('Tablet Device')),
        (HOTSPOT, ('WiFi Hotspot')),
        (PROJECTOR, ('Projector')),
        (IP_PHONE, ('IP Phone')),
        (DOC_CAM, ('Document Camera')),
        (HD_TV, ('High-Def TV')),
        (SWIVL, ('Swivl')),
        (DRONE, ('Drone')),
        (TRI_POD, ('Camera Tri-Pod')),
    )
    
    # Choices for 'manufacturer' field.
    CHOOSE      = 100
    APPLE       = 99
    CASIO       = 98
    DELL        = 97
    DJI         = 96
    EPSON       = 95
    HP          = 94
    LOGITECH    = 93
    MITEL       = 92
    PHILIPS     = 91
    SAMSUNG     = 90
    SHORETEL    = 89
    SONY        = 88
    SUPERSONIC  = 87
    SWIVL       = 86
    MANUFACTURER = (
        (CHOOSE, ('Choose Manufacturer')),
        (APPLE, ('Apple')),
        (CASIO, ('Casio')),
        (DELL, ('Dell')),
        (DJI, ('DJI')),
        (EPSON, ('Epson')),
        (HP, ('Hewlett-Packard (HP)')),
        (LOGITECH, ('Logitech')),
        (MITEL, ('Mitel')),
        (PHILIPS, ('Philips')),
        (SAMSUNG, ('Samsung')),
        (SHORETEL, ('ShoreTel')),
        (SONY, ('Sony')),
        (SUPERSONIC, ('Supersonic')),
        (SWIVL, ('Swivl'))
    )
    
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE, default=SELECT, verbose_name='Device Type')
    manufacturer = models.PositiveSmallIntegerField(choices=MANUFACTURER, default=CHOOSE)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, verbose_name='Serial Number')
    imei_number = models.PositiveBigIntegerField(verbose_name='IMEI Number')
    wlan_mac_address = models.CharField(max_length=17, verbose_name='WLAN MAC Address')
    lan_mac_address = models.CharField(max_length=17, verbose_name='LAN MAC Address')
    replacement_fee = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Replacement Fee', default=0.00)
    
    def __str__(self):
        return self.serial_number
    

class AssetTag(models.Model):
    tag_id = models.CharField(max_length=20, verbose_name='Tag ID')
    qr_code = models.ImageField(blank=True, null=True, verbose_name='QR Code')
    
    class Meta:
        verbose_name = 'Asset Tag'
        verbose_name_plural = 'Asset Tags'
    
    def __str__(self):
        return self.tag_id