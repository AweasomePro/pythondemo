# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_auto_20160923_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inviterecord',
            name='recharge_time',
            field=models.DateTimeField(blank=True, null=True, help_text='首次充值的时间'),
        ),
    ]
