# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0010_auto_20160909_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointpay',
            name='pay_method',
            field=models.IntegerField(choices=[(1, '支付宝'), (2, '微信')], default=1, help_text='支付渠道'),
        ),
    ]
