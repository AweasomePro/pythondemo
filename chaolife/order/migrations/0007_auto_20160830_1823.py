# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20160830_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbill',
            name='delay_settlement_time',
            field=models.DateTimeField(verbose_name='需要结算的日期', null=True),
        ),
        migrations.AlterField(
            model_name='orderbill',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
