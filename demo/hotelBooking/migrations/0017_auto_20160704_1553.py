# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0016_auto_20160704_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(1, 'male'), (0, 'female')], default=1, max_length=1),
        ),
    ]
