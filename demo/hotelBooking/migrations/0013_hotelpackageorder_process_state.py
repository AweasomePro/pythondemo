# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0012_auto_20160703_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(help_text='订单进行的状态', default=1, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户反悔'), (16, '代理接收了订单'), (32, '代理拒绝了订单'), (48, '代理单方面取消了订单')]),
        ),
    ]
