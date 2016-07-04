# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0020_auto_20160704_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelPackageOrderSnapShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('hotel_id', models.IntegerField()),
                ('house_id', models.IntegerField()),
                ('hotel_name', models.CharField(max_length=255)),
                ('house_name', models.CharField(max_length=255)),
                ('front_price', models.IntegerField()),
                ('need_point', models.IntegerField()),
                ('hotel_package_order', models.OneToOneField(to='hotelBooking.HotelPackageOrder')),
            ],
        ),
    ]
