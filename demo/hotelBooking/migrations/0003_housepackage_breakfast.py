# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_auto_20160711_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='housepackage',
            name='breakfast',
            field=models.IntegerField(choices=[(1, '无早'), (2, '单早'), (3, '双早')], verbose_name='breakfast type', default=1),
        ),
    ]
