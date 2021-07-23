# Generated by Django 3.2.5 on 2021-07-22 16:36

import devices.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0023_contactinfoentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrower',
            name='email',
        ),
        migrations.AddField(
            model_name='borrower',
            name='laker_email',
            field=models.EmailField(default='example@lakerschools.org', max_length=254, unique=True, validators=[devices.models.validate_laker_email], verbose_name='Laker Email Address'),
        ),
        migrations.AlterField(
            model_name='contactinfoentry',
            name='primary_phone_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Work'), (3, 'Mobile'), (2, 'Home')], null=True, verbose_name='Primary Contact Number Type'),
        ),
        migrations.AlterField(
            model_name='contactinfoentry',
            name='secondary_phone_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Work'), (3, 'Mobile'), (2, 'Home')], null=True, verbose_name='Secondary Contact Number Type'),
        ),
    ]