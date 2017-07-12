# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0008_auto_20160830_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.FloatField(default=0, verbose_name='订单总价(积分)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, '订单发起'), (2, '订单进行中'), (3, '订单取消'), (4, '订单完成')], default=1, verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.IntegerField(choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')], default=1, verbose_name='支付状态', db_index=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, related_name='seller_orders', default=1000, verbose_name='销售商', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_status',
            field=models.IntegerField(choices=[(0, '未发货'), (1, '发货中'), (2, '已收货'), (3, '无需发货')], default=0, verbose_name='运送状态', db_index=True),
        ),
    ]
