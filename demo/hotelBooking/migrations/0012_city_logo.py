# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0011_auto_20160620_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='logo',
            field=models.URLField(verbose_name='城市Logo图', default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg'),
        ),
    ]
