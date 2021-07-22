from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_email

class Asset(models.Model):
    borrower = models.ForeignKey(
        'Borrower',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
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
        blank=False,
        verbose_name='Asset Tag'
    )
    serial_number = models.CharField(
        max_length=50,
        null=True,
        blank=False,
        unique=True,
        verbose_name='Serial Number'
    )
    imei_number = models.PositiveBigIntegerField(
        null=True,
        blank=False,
        unique=True,
        verbose_name='IMEI Number'
    )
    lan_mac_address = models.CharField(
        max_length=17,
        null=True,
        blank=False,
        unique=True,
        verbose_name='LAN MAC Address',
    )
    wlan_mac_address = models.CharField(
        max_length=17,
        null=True,
        blank=False,
        unique=True,
        verbose_name='WLAN MAC Address',
    )
    
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


# Validator function for borrowers' Laker email addresses (i.e. - "student@lakerschools.org").
def validate_laker_email(value):
    if "@lakerschools.org" in value:
         return value
    else:
        raise ValidationError("Please try again with a 'lakerschools.org' email address")
    
# Validator function for borrowers' secondary email addresses.
def validate_secondary_email(value):
    try:
        validate_email(value)
        valid_email = True
    except validate_email.ValidationError:
        valid_email = False
        raise ValidationError("Please try again with a valid email address")

class Borrower(models.Model):
    borrower_type = models.ForeignKey(
        'BorrowerType',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Borrower Type'
    )
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    contact_info_entry = models.ForeignKey(
        'ContactInfoEntry',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Contact Info Entry'
    )
    laker_email = models.EmailField(
        validators=[validate_laker_email],
        max_length=254,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Laker Email Address',
    )
    secondary_email = models.EmailField(
        validators=[validate_secondary_email],
        max_length=254,
        null=True,
        blank=True,
        unique=True,
        verbose_name='Secondary Email Address',
    )
    school = models.name = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    account_balance = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        verbose_name='Account Balance',
        null=True,
        blank=False
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
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return self.name

    
class ContactInfoEntry(models.Model):
    # Choices for the 'primary_phone_type' & the 'secondary_phone_type' fields.
    WORK            = 1
    HOME            = 2
    MOBILE          = 3
    PHONE_TYPE = {
        (WORK, 'Work'),
        (HOME, 'Home'),
        (MOBILE, 'Mobile')
    }

    address_1 = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Address (line 1)',
        unique=True
    )
    address_2 = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Address (line 2)'
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    state = models.ForeignKey(
        'State',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    # Checks for proper formatting of either 5-digit or 9-digit zip codes.
    zip_code_regex = RegexValidator(regex=r"\d{5}|\d[5]-\d{4}")
    zip_code = models.CharField(
        validators=[zip_code_regex],
        max_length=10,
        null=False,
        blank=False,
        verbose_name='Zip Code'
    )
    # Checks for proper international standard formatting of phone numbers.
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    primary_phone = models.CharField(
        validators=[phone_regex],
        max_length=16,
        null=False,
        blank=False,
        verbose_name='Primary Contact Number',
    )
    primary_phone_type = models.PositiveSmallIntegerField(
        choices=PHONE_TYPE,
        null=True,
        blank=False,
        verbose_name='Primary Contact Number Type'
    )
    secondary_phone = models.CharField(
        validators=[phone_regex],
        max_length=16,
        null=True,
        blank=True,
        verbose_name='Secondary Contact Number',
    )
    secondary_phone_type = models.PositiveSmallIntegerField(
        choices=PHONE_TYPE,
        null=True,
        blank=True,
        verbose_name='Secondary Contact Number Type'
    )
    
    class Meta:
        verbose_name = 'Contact Info Entry'
        verbose_name_plural = 'Contact Info Entries'
    
    def __str__(self):
        return f"{self.address_1}, {self.city}, {self.state.abbreviation}"


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
        null=True,
        blank=False,
        verbose_name='Device Type'
    )
    device_maker = models.ForeignKey(
        'DeviceMaker',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Device Maker'
    )
    device_model = models.ForeignKey(
        'DeviceModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Device Model'
    )
    
    def __str__(self):
        return f"{self.device_maker} - {self.device_model}"
    
    
class DeviceMaker(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Device Maker'
        verbose_name_plural = 'Device Makers'

    def __str__(self):
        return self.name

    
class DeviceModel(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    
    class Meta:
        verbose_name = 'Device Model'
        verbose_name_plural = 'Device Models'
    
    def __str__(self):
        return self.name


class DeviceType(models.Model):
    category_name = models.CharField(
        max_length=50,
        default='Enter category name here',
        null=False,
        blank=False,
        unique=True,
        verbose_name='Category Name',
    )
    sn_available = models.BooleanField(
        default=False,
        verbose_name='S/N (Serial Number) available for this device'
    )
    imei_available = models.BooleanField(
        default=False,
        verbose_name='IMEI (International Mobile Equipment Identity) number available for this device'
    )
    lan_mac_available = models.BooleanField(
        default=False,
        verbose_name='LAN (ethernet) MAC address available for this device'
    )
    wlan_mac_available = models.BooleanField(
        default=False,
        verbose_name='WLAN (wireless) MAC address available for this device'
    )
    live_stream = models.BooleanField(
        default=False,
        verbose_name='Used for live-streamed school events'
    )
    inperson_learning = models.BooleanField(
        default=False,
        verbose_name='Used for in-person learning'
    )
    virtual_learning = models.BooleanField(
        default=False,
        verbose_name='Used for virtual learning'
    )

    class Meta:
        verbose_name = 'Device Type'
        verbose_name_plural = 'Device Types'
        
    def __str__(self):
        return self.category_name


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