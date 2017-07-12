# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0016_auto_20160831_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(default=1, help_text='详细的订单进行的状态', db_index=True, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了'), (-100, '代理超时确认，自动取消'), (20, '客户入住中(ing)'), (30, '到达ckeckoutTime之后(表示等待结算)'), (40, '交易积分已转到代理商账号'), (-201, '退款赔付ing'), (-202, '退款部分完成'), (-200, '退款完成')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=1, verbose_name='订单状态', choices=[(1, '订单发起'), (2, '订单进行中'), (3, '订单取消'), (5, '订单赔付完成'), (4, '订单完成')]),
        ),
    ]
