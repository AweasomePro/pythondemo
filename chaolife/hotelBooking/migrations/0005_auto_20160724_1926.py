# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0004_auto_20160724_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelimg',
            name='img_url',
        ),
        migrations.RemoveField(
            model_name='roomimg',
            name='img_url',
        ),
    ]
