# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import chaolife.models.plugins
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0008_auto_20160830_1034'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0002_auto_20160818_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderRefund',
            fields=[
                ('code', models.CharField(help_text='退款编号', default=chaolife.models.plugins.HotelOrderNumberGenerator.get_next_refund_number, max_length=32, serialize=False, primary_key=True)),
                ('order_des', models.CharField(max_length=100, verbose_name='本次交易描述')),
                ('proposer_refund_declaration', models.CharField(max_length=200, verbose_name='用户退款说明')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('refund_reason', models.IntegerField(choices=[(1, '无法入住'), (0, '其他')], verbose_name='退货原因')),
                ('state', models.IntegerField(choices=[(1, '申请中'), (2, '接收退货'), (-1, '拒绝退货'), (1, '退货完成')], verbose_name='申请状态')),
                ('detail_state', models.IntegerField(verbose_name='详细状态')),
                ('success_time', models.DateTimeField(verbose_name='退款成功时间')),
                ('refund_points', models.FloatField(verbose_name='退还积分')),
                ('order', models.ForeignKey(to='chaolife.Order', verbose_name='订单')),
                ('product', models.ForeignKey(to='chaolife.Product', verbose_name='商品')),
                ('proposer', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='申请人')),
                ('seller', models.ForeignKey(related_name='sellerorders', to=settings.AUTH_USER_MODEL, verbose_name='商家')),
            ],
        ),
    ]
