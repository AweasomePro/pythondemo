# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20160831_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderrefund',
            name='losses_money_currency',
        ),
        migrations.AlterField(
            model_name='orderbill',
            name='commission',
            field=models.FloatField(default=0, verbose_name='佣金(积分)'),
        ),
        migrations.AlterField(
            model_name='orderbill',
            name='seller_gains',
            field=models.FloatField(verbose_name='卖家收益积分', help_text='在产生积分赔付的情况下，该值可能为负'),
        ),
        migrations.AlterField(
            model_name='orderrefund',
            name='losses_money',
            field=models.FloatField(default=0, verbose_name='赔付现金金额'),
        ),
        migrations.AlterField(
            model_name='orderrefund',
            name='refunded',
            field=models.BooleanField(default=False, help_text='这个状态不得重复更改,否则会造成积分多次赔付的情况', verbose_name='积分已赔付到账?'),
        ),
        migrations.AlterField(
            model_name='orderrefund',
            name='state',
            field=models.IntegerField(verbose_name='申请状态', choices=[(1, '申请中'), (2, '接收退货(款)'), (3, '赔付部分到账'), (-1, '拒绝退货(款)'), (100, '退货完成')]),
        ),
    ]
