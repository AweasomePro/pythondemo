# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20160901_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderbill',
            options={'verbose_name_plural': '订单结算', 'verbose_name': '订单结算'},
        ),
        migrations.AlterModelOptions(
            name='orderrefund',
            options={'verbose_name_plural': '订单赔付', 'verbose_name': '订单赔付'},
        ),
        migrations.AlterField(
            model_name='orderbill',
            name='capital_settlement',
            field=models.IntegerField(choices=[(1, '立即结算'), (2, '延迟结算')], help_text='资金结算方式，有包括立即结算，和延时结算', verbose_name='商家结算方式'),
        ),
    ]
