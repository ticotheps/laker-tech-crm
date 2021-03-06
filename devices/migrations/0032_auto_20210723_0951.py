# Generated by Django 3.2.5 on 2021-07-23 09:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0031_auto_20210723_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfoentry',
            name='primary_phone_type',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Home'), (1, 'Work'), (3, 'Mobile')], null=True, verbose_name='Primary Phone Number Type'),
        ),
        migrations.AlterField(
            model_name='contactinfoentry',
            name='secondary_phone_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(2, 'Home'), (1, 'Work'), (3, 'Mobile')], null=True, verbose_name='Secondary Phone Number Type'),
        ),
        migrations.AlterField(
            model_name='graduationyear',
            name='year',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex='^(202|203|204|205|206|207|208|209)\\d{1}$')], verbose_name='Graduation Year'),
        ),
    ]
