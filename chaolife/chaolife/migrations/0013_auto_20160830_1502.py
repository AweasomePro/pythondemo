# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0012_auto_20160830_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelpackageorder',
            name='closed',
        ),
        migrations.RemoveField(
            model_name='hotelpackageorder',
            name='success',
        ),
        migrations.AddField(
            model_name='order',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='success',
            field=models.BooleanField(help_text='订单完成', default=False),
        ),
    ]
