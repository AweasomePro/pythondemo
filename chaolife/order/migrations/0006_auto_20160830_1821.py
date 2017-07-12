# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0005_auto_20160830_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbill',
            name='delay_settlement_time',
            field=models.DateTimeField(verbose_name='需要结算的日期', default=datetime.datetime(2016, 8, 30, 18, 20, 44, 485425)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderbill',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=7),
            preserve_default=False,
        ),
    ]
