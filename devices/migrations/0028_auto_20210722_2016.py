# Generated by Django 3.2.5 on 2021-07-22 20:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0027_auto_20210722_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Category Name')),
                ('sn_available', models.BooleanField(default=False, verbose_name='S/N (Serial Number) available for this device')),
                ('imei_available', models.BooleanField(default=False, verbose_name='IMEI (International Mobile Equipment Identity) number available for this device')),
                ('lan_mac_available', models.BooleanField(default=False, verbose_name='LAN (ethernet) MAC address available for this device')),
                ('wlan_mac_available', models.BooleanField(default=False, verbose_name='WLAN (wireless) MAC address available for this device')),
                ('live_stream', models.BooleanField(default=False, verbose_name='Used for live-streamed school events')),
                ('inperson_learning', models.BooleanField(default=False, verbose_name='Used for in-person learning')),
                ('virtual_learning', models.BooleanField(default=False, verbose_name='Used for virtual learning')),
            ],
            options={
                'verbose_name': 'Device Category',
                'verbose_name_plural': 'Device Categories',
            },
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Device Model',
                'verbose_name_plural': 'Device Models',
            },
        ),
        migrations.RemoveField(
            model_name='device',
            name='device_type',
        ),
        migrations.RemoveField(
            model_name='device',
            name='model_name',
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_tag',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.assettag', verbose_name='Asset Tag'),
        ),
        migrations.AlterField(
            model_name='contactinfoentry',
            name='primary_phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Primary Phone Number'),
        ),
        migrations.AlterField(
            model_name='contactinfoentry',
            name='primary_phone_type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Mobile'), (1, 'Work'), (2, 'Home')], null=True, verbose_name='Primary Phone Number Type'),
        ),
        migrations.AlterField(
            model_name='contactinfoentry',
            name='secondary_phone',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Secondary Phone Number'),
        ),
        migrations.AlterField(
            model_name='contactinfoentry',
            name='secondary_phone_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(3, 'Mobile'), (1, 'Work'), (2, 'Home')], null=True, verbose_name='Secondary Phone Number Type'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_maker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.devicemaker', verbose_name='Device Maker'),
        ),
        migrations.DeleteModel(
            name='DeviceType',
        ),
        migrations.AddField(
            model_name='device',
            name='device_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.devicecategory', verbose_name='Device Category'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.devicemodel', verbose_name='Device Model'),
        ),
    ]
