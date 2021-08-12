from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_email

class Asset(models.Model):
    # Choices for the 'status' field.
    CHECKED_OUT     = 1
    DECOMMISIONED   = 2
    IN_STOCK        = 3
    LOST            = 4
    REPAIR          = 5
    STOLEN          = 6
    STATUS = {
        (REPAIR, 'Under Repair'),
        (STOLEN, 'Stolen'),
        (LOST, 'Lost'),
        (IN_STOCK, 'In Stock'),
        (DECOMMISIONED, 'Decommissioned'),
        (CHECKED_OUT, 'Checked Out'),
    }
    
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
        blank=True,
        verbose_name='Asset Tag'
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
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=IN_STOCK,
        null=False,
        blank=False,
        verbose_name='Status'
    )
    
    def __str__(self):
        return f"{self.asset_tag} (S/N: {self.serial_number})"


class AssetTag(models.Model):
    tag_id = models.CharField(max_length=20, verbose_name='Tag ID', unique=True)
    qr_code = models.ImageField(blank=True, null=True, verbose_name='QR Code')
    
    class Meta:
        verbose_name = 'Asset Tag'
        verbose_name_plural = 'Asset Tags'
    
    def __str__(self):
        return self.tag_id


# Validator function to ensure an email address contains the "lakerschools.org" domain.
def validate_laker_email(value):
    if "@lakerschools.org" in value:
         return value
    else:
        raise ValidationError("Please try again with a 'lakerschools.org' email address")
    
# Validator function to ensure an email address contains the proper components.
def validate_email_address(value):
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
        blank=True,
        verbose_name='Borrower Type'    
    )
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    graduation_year = models.ForeignKey(
        'GraduationYear',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Graduation Year (if applicable)'
    )
    laker_email = models.EmailField(
        max_length=254,
        verbose_name='Laker Email Address',
        default='example@lakerschools.org',
        null=False,
        blank=False,
        unique=True,
        validators=[validate_laker_email, validate_email_address]
    )
    secondary_email = models.EmailField(
        max_length=254,
        verbose_name='Secondary Email Address',
        null=True,
        blank=True,
        unique=True,
        validators=[validate_email_address]
    )
    school = models.name = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='School of Enrollment (if applicable)'
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
        verbose_name='Primary Phone Number',
        null=False,
        blank=False
    )
    primary_phone_type = models.PositiveSmallIntegerField(
        choices=PHONE_TYPE,
        null=True,
        blank=False,
        verbose_name='Primary Phone Number Type'
    )
    secondary_phone = models.CharField(
        validators=[phone_regex],
        max_length=16,
        verbose_name='Secondary Phone Number',
        null=True,
        blank=True
    )
    secondary_phone_type = models.PositiveSmallIntegerField(
        choices=PHONE_TYPE,
        null=True,
        blank=True,
        verbose_name='Secondary Phone Number Type'
    )
    
    class Meta:
        verbose_name = 'Contact Info Entry'
        verbose_name_plural = 'Contact Info Entries'
    
    def __str__(self):
        return f"{self.address_1}, {self.city}, {self.state.abbreviation}"


class Device(models.Model):
    device_category = models.ForeignKey(
        'DeviceCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Device Category'
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
    replacement_fee = models.DecimalField(
        decimal_places=2,
        default=0.00,
        max_digits=6,
        verbose_name='Replacement Fee'
    )
    
    def __str__(self):
        return f"{self.device_maker} - {self.device_model}"
    
    
class DeviceCategory(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Category Name',
        null=False,
        blank=False,
        unique=True
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
        verbose_name = 'Device Category'
        verbose_name_plural = 'Device Categories'
        
    def __str__(self):
        return self.name 
    
    
class DeviceMaker(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Device Maker'
        verbose_name_plural = 'Device Makers'

    def __str__(self):
        return self.name
    
    
class DeviceModel(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False, unique=True)
    
    class Meta:
        verbose_name = 'Device Model'
        verbose_name_plural = 'Device Models'
    
    def __str__(self):
        return self.name


class GraduationYear(models.Model):
    # Checks for proper formatting of a valid 4-digit graduation year up to 2099.
    year_regex = RegexValidator(regex=r"^(202|203|204|205|206|207|208|209)\d{1}$")
    year = models.CharField(
        validators=[year_regex],
        max_length=4,
        null=False,
        blank=False,
        verbose_name='Graduation Year'
    )
    
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
    building = models.ForeignKey(
        'Building',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='School Building'
    )
    
    def __str__(self):
        return f"{self.name} - {self.building}"
    

class State(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True, unique=True)
    abbreviation = models.CharField(max_length=2, null=False, blank=True, unique=True)
    
    def __str__(self):
        return f"{self.abbreviation} ({self.name})"
    
    
class Transaction(models.Model):
    # Choices for the 'action' field.
    CHECK_IN        = 1
    CHECK_OUT       = 2
    DAMAGED         = 3
    DYSFUNCTIONAL   = 4
    LOST            = 5
    STOLEN          = 6
    ACTION = {
        (STOLEN, 'Report Stolen'),
        (LOST, 'Report Lost'),
        (DYSFUNCTIONAL, 'Report Dysfunctional'),
        (DAMAGED, 'Report Damage'),
        (CHECK_OUT, 'Check-Out'),
        (CHECK_IN, 'Check-In'),
    }
    borrower = models.OneToOneField(
        'Borrower',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    asset = models.OneToOneField(
        'Asset',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    action = models.PositiveSmallIntegerField(
        choices=ACTION,
        null=True,
        blank=False,
    )
    transaction_date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
        verbose_name='Transaction Date'
    )

    def __str__(self):
        return f"{self.borrower} - {self.action}"