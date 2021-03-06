# Generated by Django 3.2.5 on 2021-07-14 18:58

import devices.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0011_alter_device_device_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[devices.models.validate_laker_email], verbose_name='Email Address')),
                ('account_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='Account Balance')),
            ],
        ),
    ]
