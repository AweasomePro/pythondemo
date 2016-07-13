# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0003_auto_20160713_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='installation',
            name='active',
            field=models.BooleanField(verbose_name='active?', default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(verbose_name='password', max_length=128),
        ),
    ]
