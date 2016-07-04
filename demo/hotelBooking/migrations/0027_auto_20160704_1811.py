# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0026_auto_20160704_1810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotelpackageordersnapshot',
            old_name='hotell_package_order',
            new_name='hotel_package_order',
        ),
    ]
