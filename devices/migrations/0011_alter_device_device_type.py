# Generated by Django 3.2.5 on 2021-07-06 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0010_auto_20210705_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Select Device Type'), (2, 'Desktop PC'), (3, 'Document Camera'), (4, 'Drone'), (5, 'High-Def TV'), (6, 'IP Phone'), (7, 'Laptop PC (>=8GB RAM)'), (8, 'Laptop Charger'), (9, 'Notebook PC (<8GB RAM)'), (10, 'Notebook Charger'), (11, 'Projector'), (12, 'Swivl'), (13, 'Tablet'), (14, 'Tablet Charger'), (15, 'Tri-Pod Stand'), (16, 'WiFi Hotspot')], default=1, verbose_name='Device Type'),
        ),
    ]
