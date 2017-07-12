# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0013_auto_20160830_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(db_index=True, default=1, help_text='详细的订单进行的状态', choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了'), (-100, '代理超时确认，自动取消'), (20, '客户入住中(ing)'), (30, '到达ckeckoutTime之后(表示等待结算)'), (40, '交易积分已转到代理商账号')]),
        ),
    ]
