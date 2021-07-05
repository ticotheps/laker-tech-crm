from django.db import models

class Device(models.Model):
    # Choices for 'device_type' field.
    SELECT              = 1
    DESKTOP             = 2
    DOC_CAM             = 3
    DRONE               = 4
    HD_TV               = 5
    HOTSPOT             = 6
    IP_PHONE            = 7
    LAPTOP              = 8
    LAPTOP_CHARGER      = 9
    NOTEBOOK            = 10
    NOTEBOOK_CHARGER    = 11
    PROJECTOR           = 12
    SWIVL               = 13
    TABLET              = 14
    TABLET_CHARGER      = 15
    TRI_POD             = 16
    DEVICE_TYPE = (
        (SELECT, ('Select Device Type')),
        (DESKTOP, ('Desktop PC')),
        (DOC_CAM, ('Document Camera')),
        (DRONE, ('Drone')),
        (HD_TV, ('High-Def TV')),
        (HOTSPOT, ('WiFi Hotspot')),
        (IP_PHONE, ('IP Phone')),
        # 'Laptop PC' = a portable computer with >= 8GB RAM (i.e. - older Lenovo ThinkPads).
        (LAPTOP, ('Laptop PC (>=8GB RAM)')),
        (LAPTOP_CHARGER, ('Laptop Charger')),
        # 'Notebook PC' = a portable computer with < 8GB RAM (i.e. - Chromebooks).
        (NOTEBOOK, ('Notebook PC (<8GB RAM)')),            
        (NOTEBOOK_CHARGER, ('Notebook Charger')),
        (PROJECTOR, ('Projector')),
        (SWIVL, ('Swivl')),
        (TABLET, ('Tablet')),
        (TABLET_CHARGER, ('Tablet Charger')),
        (TRI_POD, ('Tri-Pod Stand')),
    )

    # Choices for 'make_and_model' field.
    CHOOSE              = 100
    APPLE_A1432_TAB     = 99
    APPLE_A1489_TAB     = 98
    APPLE_A1893_TAB     = 97
    APPLE_A2270_TAB     = 96
    DELL_3020_PC        = 95
    DELL_3100_NB        = 94
    HP_11_A_NB          = 93
    HP_11_V_NB          = 92
    HP_400_PC           = 91
    HP_600_PC           = 90
    LENOVO_300E_NB      = 89
    LENOVO_L450_LAP     = 88
    LENOVO_L540_LAP     = 87

    MAKE_AND_MODEL = (
        (CHOOSE, ('Choose Device Make - Model')),
        (APPLE_A1432_TAB, ('Apple - iPad mini (1st Gen, Model A1432)')),
        (APPLE_A1489_TAB, ('Apple - iPad mini 2 (2nd Gen, Model A1489)')),
        (APPLE_A1893_TAB, ('Apple - iPad (6th Gen, Model A1893)')),
        (APPLE_A2270_TAB, ('Apple - iPad (8th Gen, Model A2270)')),       
        (DELL_3020_PC, ('Dell - OptiPlex 3020 (Teacher-grade PC)')),
        (DELL_3100_NB, ('Dell - Chromebook 3100 (USB-C charger)')),
        (HP_11_A_NB, ('HP - Chromebook 11A G8 EE (USB-C charger)')),
        (HP_11_V_NB, ('HP - Chromebook 11-v031nr (AC Adapter, blue-tip plug)')),
        (HP_400_PC, ('HP - ProDesk 400 G6 SFF (Lab-grade PC)')),
        (HP_600_PC, ('HP - ProDesk 600 G5 SFF (Teacher-grade PC)')),
        (LENOVO_300E_NB, ('Lenovo - 300e (2nd Gen.)')),
        (LENOVO_L450_LAP, ('Lenovo - ThinkPad L450')),
        (LENOVO_L540_LAP, ('Lenovo - ThinkPad L540'))
    )
    
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE, default=SELECT, verbose_name='Device Type')
    make_and_model = models.PositiveSmallIntegerField(choices=MAKE_AND_MODEL, default=CHOOSE, verbose_name='Make & Model')
    serial_number = models.CharField(max_length=50, verbose_name='Serial Number')
    imei_number = models.PositiveBigIntegerField(verbose_name='IMEI Number', null=True, blank=True)
    wlan_mac_address = models.CharField(max_length=17, verbose_name='WLAN MAC Address', null=True, blank=True)
    lan_mac_address = models.CharField(max_length=17, verbose_name='LAN MAC Address', null=True, blank=True)
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