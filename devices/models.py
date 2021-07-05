from django.db import models

class Device(models.Model):
    # Choices for 'device_type' field.
    SELECT              = 1
    DESKTOP             = 2
    LAPTOP              = 3
    LAPTOP_CHARGER      = 4
    NOTEBOOK            = 5
    NOTEBOOK_CHARGER    = 6
    TABLET              = 7
    TABLET_CHARGER      = 8
    HOTSPOT             = 9
    PROJECTOR           = 10 
    IP_PHONE            = 11
    DOC_CAM             = 12
    HD_TV               = 13
    SWIVL               = 14
    DRONE               = 15
    TRI_POD             = 16
    DEVICE_TYPE = (
        (SELECT, ('Select Device Type')),
        (DESKTOP, ('Desktop PC')),
        (LAPTOP, ('Laptop PC (>=8GB RAM)')),    # 'Laptop PC' = a portable computer with >= 8GB RAM (i.e. - older Lenovo ThinkPads).
        (LAPTOP_CHARGER, ('Laptop Charger')),
        (NOTEBOOK, ('Notebook PC (<8GB RAM)')),    # 'Notebook PC' = a portable computer with < 8GB RAM (i.e. - Chromebooks).            
        (NOTEBOOK_CHARGER, ('Notebook Charger')),
        (TABLET, ('Tablet')),
        (TABLET_CHARGER, ('Tablet Charger')),
        (HOTSPOT, ('WiFi Hotspot')),
        (PROJECTOR, ('Projector')),
        (IP_PHONE, ('IP Phone')),
        (DOC_CAM, ('Document Camera')),
        (HD_TV, ('High-Def TV')),
        (SWIVL, ('Swivl')),
        (DRONE, ('Drone')),
        (TRI_POD, ('Tri-Pod Stand')),
    )

    # Choices for 'make_and_model' field.
    CHOOSE              = 100
    HP_11_A_NB          = 99
    DELL_3100_NB        = 98
    HP_11_V_NB          = 97
    APPLE_A1432_TAB     = 96
    APPLE_A1489_TAB     = 95
    LENOVO_300E_NB      = 94
    LENOVO_L450_LAP     = 93
    LENOVO_L540_LAP     = 92
    HP_400_PC           = 91
    HP_600_PC           = 90
    DELL_3020_PC        = 89
    APPLE_A1893_TAB     = 88
    APPLE_A2270_TAB     = 87
    MAKE_AND_MODEL = (
        (CHOOSE, ('Choose Device Make - Model')),
        (HP_11_A_NB, ('HP - Chromebook 11A G8 EE (USB-C charger)')),
        (DELL_3100_NB, ('Dell - Chromebook 3100 (USB-C charger)')),
        (HP_11_V_NB, ('HP - Chromebook 11-v031nr (AC Adapter, blue-tip plug)')),
        (APPLE_A1432_TAB, ('Apple - iPad mini (1st Gen, Model A1432)')),
        (APPLE_A1489_TAB, ('Apple - iPad mini 2 (2nd Gen, Model A1489)')),
        (LENOVO_300E_NB, ('Lenovo - 300e (2nd Gen.)')),
        (LENOVO_L450_LAP, ('Lenovo - ThinkPad L450')),
        (LENOVO_L540_LAP, ('Lenovo - ThinkPad L540')),
        (HP_400_PC, ('HP - ProDesk 400 G6 SFF (Lab-grade PC)')),
        (HP_600_PC, ('HP - ProDesk 600 G5 SFF (Teacher-grade PC)')),
        (DELL_3020_PC, ('Dell - OptiPlex 3020 (Teacher-grade PC)')),
        (APPLE_A1893_TAB, ('Apple - iPad (6th Gen, Model A1893)')),
        (APPLE_A2270_TAB, ('Apple - iPad (8th Gen, Model A2270)')),
    )
    
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE, default=SELECT, verbose_name='Device Type')
    make_and_model = models.PositiveSmallIntegerField(choices=MAKE_AND_MODEL, default=CHOOSE, verbose_name='Make & Model')
    serial_number = models.CharField(max_length=50, verbose_name='Serial Number')
    imei_number = models.PositiveBigIntegerField(verbose_name='IMEI Number', null=True, blank=True)
    wlan_mac_address = models.CharField(max_length=17, verbose_name='WLAN MAC Address', null=True, blank=True)
    lan_mac_address = models.CharField(max_length=17, verbose_name='LAN MAC Address', null=True, blank=True)
    replacement_fee = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Replacement Fee', default=0.00)
    asset_tag = models.OneToOneField('AssetTag', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Asset Tag')
    
    def __str__(self):
        return self.serial_number
    

class AssetTag(models.Model):
    tag_id = models.CharField(max_length=20, verbose_name='Tag ID', unique=True)
    qr_code = models.ImageField(blank=True, null=True, verbose_name='QR Code')
    
    class Meta:
        verbose_name = 'Asset Tag'
        verbose_name_plural = 'Asset Tags'
    
    def __str__(self):
        return self.tag_id