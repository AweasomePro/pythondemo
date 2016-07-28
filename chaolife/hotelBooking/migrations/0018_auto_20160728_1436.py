# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0017_roompackage_bill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='Smoking',
            new_name='smoking',
        ),
    ]
