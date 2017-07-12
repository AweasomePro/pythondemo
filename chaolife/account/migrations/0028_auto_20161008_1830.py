# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.fiels


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_auto_20160926_1037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='installation',
            options={'verbose_name_plural': '设备', 'ordering': ('user', '-timeZone'), 'verbose_name': 'App已安装设备'},
        ),
        migrations.AlterField(
            model_name='installation',
            name='channels',
            field=common.fiels.ListField(default=['customer'], verbose_name='订阅渠道', null=True),
        ),
    ]
