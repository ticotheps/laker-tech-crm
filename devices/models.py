from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Asset(models.Model):
    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    asset_tag = models.OneToOneField(
        'AssetTag',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    borrower = models.ForeignKey(
        'Borrower',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    serial_number = models.CharField(
        max_length=50,
        verbose_name='Serial Number'
    )
    imei_number = models.PositiveBigIntegerField(
        verbose_name='IMEI Number',
        null=True,
        blank=True
    )
    lan_mac_address = models.CharField(
        max_length=17,
        verbose_name='LAN MAC Address',
        null=True,
        blank=True
    )
    wlan_mac_address = models.CharField(
        max_length=17,
        verbose_name='WLAN MAC Address',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.asset_tag


class AssetTag(models.Model):
    tag_id = models.CharField(max_length=20, verbose_name='Tag ID', unique=True)
    qr_code = models.ImageField(blank=True, null=True, verbose_name='QR Code')
    
    class Meta:
        verbose_name = 'Asset Tag'
        verbose_name_plural = 'Asset Tags'
    
    def __str__(self):
        return self.tag_id


# Validator function for borrowers' email addresses (i.e. - "student@lakerschools.org").
def validate_borrower_email(value):
    if "@lakerschools.org" in value:
         return value
    else:
        raise ValidationError("Please try again with a 'lakerschools.org' email address")


class Borrower(models.Model):
    borrower_type = models.name = models.ForeignKey(
        'BorrowerType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True    
    )
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    email = models.EmailField(
        max_length=254,
        verbose_name='Email Address',
        unique=True,
        validators=[validate_borrower_email]
    )
    school = models.name = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    account_balance = models.DecimalField(
        decimal_places=2,
        default=0.00,
        max_digits=6,
        verbose_name='Account Balance'
    )
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
    
class BorrowerType(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False
    )
    
    class Meta:
        verbose_name = 'Borrower Type'
        verbose_name_plural = 'Borrower Types'
        
    def __str__(self):
        return self.name
    

class Building(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False
    )
    
    def __str__(self):
        return self.name
    

class City(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True, unique=True)
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return self.name

    
# class ContactInfo(models.Model):
#     # Choices for the 'phone_number_1_type' & the 'phone_number_2_type' fields.
#     SELECT          = 0
#     WORK            = 1
#     HOME            = 2
#     CELL            = 3
#     PHONE_NUMBER_TYPE = {
#         (SELECT, 'Select type of phone number'),
#         (WORK, 'Work'),
#         (HOME, 'Home'),
#         (CELL, 'Cell/Mobile')
#     }

#     address_1 = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#         verbose_name='Address (line 1)'
#     )
#     address_2 = models.CharField(
#         max_length=50,
#         null=True,
#         blank=True,
#         verbose_name='Address (line 2)'
#     )
    # city = models.ForeignKey(
    #     'City',
    #     on_delete=models.CASCADE,
    #     null=False,
    #     blank=False
    # )
    # state = models.ForeignKey(
    #     'State',
    #     on_delete=models.CASCADE,
    #     null=False,
    #     blank=False
    # )
    # zip_code = models.PositiveIntegerField(
    #     null=False,
    #     blank=False,
    #     verbose_name='Zip Code'
    # )
    # # Checks for proper international standard formatting of phone numbers.
    # phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    # phone_number_1 = models.CharField(
    #     validators=[phoneNumberRegex],
    #     max_length=16,
    #     unique=True,
    #     verbose_name='Phone Number #1',
    #     null=False,
    #     blank=False
    # )
    # phone_number_1_type = models.PositiveSmallIntegerField(
    #     choices=PHONE_NUMBER_TYPE,
    #     default=SELECT,
    #     null=False,
    #     blank=False,
    #     verbose_name='Phone Number #1 Type'
    # )
    # phone_number_2 = models.CharField(
    #     validators=[phoneNumberRegex],
    #     max_length=16,
    #     unique=True,
    #     verbose_name='Phone Number #2',
    #     null=True,
    #     blank=True
    # )
    # phone_number_2_type = models.PositiveSmallIntegerField(
    #     choices=PHONE_NUMBER_TYPE,
    #     null=True,
    #     blank=True,
    #     verbose_name='Phone Number #2 Type'
    # )
    
    # class Meta:
    #     verbose_name = 'Contact Information'
    #     verbose_name_plural = 'Contact Information'
    
    # def __str__(self):
    #     return self.phone_number_1


class Device(models.Model):
    # # Choices for 'make_and_model' field.
    # CHOOSE              = 100
    # APPLE_A1432_TAB     = 99
    # APPLE_A1489_TAB     = 98
    # APPLE_A1893_TAB     = 97
    # APPLE_A2270_TAB     = 96
    # DELL_3020_PC        = 95
    # DELL_3100_NB        = 94
    # HP_11_A_NB          = 93
    # HP_11_V_NB          = 92
    # HP_400_PC           = 91
    # HP_600_PC           = 90
    # LENOVO_300E_NB      = 89
    # LENOVO_L450_LAP     = 88
    # LENOVO_L540_LAP     = 87

    # MAKE_AND_MODEL = (
    #     (CHOOSE, ('Choose Device Make - Model')),
    #     (APPLE_A1432_TAB, ('Apple - iPad mini (1st Gen, Model A1432)')),
    #     (APPLE_A1489_TAB, ('Apple - iPad mini 2 (2nd Gen, Model A1489)')),
    #     (APPLE_A1893_TAB, ('Apple - iPad (6th Gen, Model A1893)')),
    #     (APPLE_A2270_TAB, ('Apple - iPad (8th Gen, Model A2270)')),       
    #     (DELL_3020_PC, ('Dell - OptiPlex 3020 (Teacher-grade PC)')),
    #     (DELL_3100_NB, ('Dell - Chromebook 3100 (USB-C charger)')),
    #     (HP_11_A_NB, ('HP - Chromebook 11A G8 EE (USB-C charger)')),
    #     (HP_11_V_NB, ('HP - Chromebook 11-v031nr (AC Adapter, blue-tip plug)')),
    #     (HP_400_PC, ('HP - ProDesk 400 G6 SFF (Lab-grade PC)')),
    #     (HP_600_PC, ('HP - ProDesk 600 G5 SFF (Teacher-grade PC)')),
    #     (LENOVO_300E_NB, ('Lenovo - 300e (2nd Gen.)')),
    #     (LENOVO_L450_LAP, ('Lenovo - ThinkPad L450')),
    #     (LENOVO_L540_LAP, ('Lenovo - ThinkPad L540'))
    # )
    
    device_type = models.OneToOneField(
        'DeviceType',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Device Type'
    )
    manufacturer = models.CharField(max_length=30, verbose_name='Manufacturer', unique=True, null=True, blank=True)
    model_name = models.CharField(max_length=30, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.manufacturer} - {self.model_name}"


class DeviceType(models.Model):
    type = models.CharField(
        max_length=50,
        verbose_name='Type of Device',
        null=False,
        blank=False,
        unique=True
    )
    sn_available = models.BooleanField(verbose_name='S/N (Serial Number) available for this device')
    imei_available = models.BooleanField(verbose_name='IMEI (International Mobile Equipment Identity) number available for this device')
    lan_mac_available = models.BooleanField(verbose_name='LAN (ethernet) MAC address available for this device')
    wlan_mac_available = models.BooleanField(verbose_name='WLAN (wireless) MAC address available for this device')
    live_stream = models.BooleanField(verbose_name='Used for live-streamed school events')
    inperson_learning = models.BooleanField(verbose_name='Used for in-person learning')
    virtual_learning = models.BooleanField(verbose_name='Used for virtual learning')

    class Meta:
        verbose_name = 'Device Type'
        verbose_name_plural = 'Device Types'
        
    def __str__(self):
        return self.type


class GraduationYear(models.Model):
    year = models.PositiveSmallIntegerField(verbose_name='Graduation Year', null=False, blank=False)
    
    class Meta:
        verbose_name = 'Graduation Year'
        verbose_name_plural = 'Graduation Years'
    
    def __str__(self):
        return self.year


class School(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='School Name'
    )
    building = models.name = models.ForeignKey(
        'Building',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='School Building'
    )
    
    def __str__(self):
        return self.name
    

class State(models.Model):
    name = models.CharField(max_length=20, null=False, blank=True, unique=True)
    abbreviation = models.CharField(max_length=2, null=False, blank=True, unique=True)
    
    def __str__(self):
        return self.name