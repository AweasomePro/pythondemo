# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0006_auto_20160720_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosedHotelPackageOrder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('hotelBooking.hotelpackageorder',),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(default=1, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (16, '代理接收了订单,但是用户尚未入住'), (32, '代理拒绝了订单'), (48, '代理提前表示某些原因导致不能入住了')], help_text='订单进行的状态'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(default=1, choices=[(1, '顾客'), (2, '酒店代理合作伙伴')], help_text='该账号的角色标识'),
        ),
    ]
