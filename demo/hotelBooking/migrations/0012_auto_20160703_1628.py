# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0011_auto_20160703_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='identifier',
        ),
        migrations.RemoveField(
            model_name='order',
            name='reference_number',
        ),
        migrations.AddField(
            model_name='housepackage',
            name='month_state',
            field=models.IntegerField(default=0),
        ),
    ]
