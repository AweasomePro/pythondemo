# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0015_auto_20160704_1448'),
    ]

    operations = [

        migrations.AddField(
            model_name='hotelpackageordersnapshot',
            name='house_package_order',
            field=models.OneToOneField(default=1, to='hotelBooking.HotelPackageOrder'),
            preserve_default=False,
        ),
    ]
