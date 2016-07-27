# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0007_auto_20160725_1433'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HotelOrderNumberGenerator',
        ),
        migrations.RemoveField(
            model_name='pay',
            name='user',
        ),
        migrations.DeleteModel(
            name='test',
        ),
        migrations.DeleteModel(
            name='Pay',
        ),
    ]
