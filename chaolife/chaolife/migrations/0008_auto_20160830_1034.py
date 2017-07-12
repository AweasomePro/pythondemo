# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0007_auto_20160822_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpackageorder',
            name='state',
            field=models.IntegerField(default=0, verbose_name='订单状态', help_text='订单状态,只包含了基本的<申请，进行，完成，>状态'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了'), (-100, '代理超时确认，自动取消'), (20, '客户入住中(ing)'), (30, '到达ckeckoutTime之后'), (40, '交易积分已转到代理商账号')], db_index=True, default=1, help_text='详细的订单进行的状态'),
        ),
    ]
