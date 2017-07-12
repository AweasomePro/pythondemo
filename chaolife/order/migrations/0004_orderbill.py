# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0009_auto_20160830_1359'),
        ('order', '0003_orderrefund'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBill',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')),
                ('commission', models.FloatField(verbose_name='佣金(积分)')),
                ('order_amount', models.FloatField(verbose_name='订单总额')),
                ('refund_amount', models.FloatField(verbose_name='退单金额', help_text='退单金额，可能是用户取消订单，退还的金额')),
                ('capital_settlement', models.IntegerField(verbose_name='商家结算方式', help_text='资金结算方式，有包括立即结算，和延时结算')),
                ('seller_gains', models.FloatField(verbose_name='卖家收益积分')),
                ('settled', models.BooleanField(verbose_name='已结算?', default=False, help_text='是否已结算')),
                ('settled_at', model_utils.fields.MonitorField(default=django.utils.timezone.now, when=set([True]), monitor=models.BooleanField(verbose_name='已结算?', default=False, help_text='是否已结算'))),
                ('order', models.OneToOneField(to='chaolife.Order')),
            ],
        ),
    ]
