# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0007_auto_20160721_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了')], help_text='订单进行的状态', default=1),
        ),
        migrations.AlterField(
            model_name='installation',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name='绑定用户', to_field='phone_number'),
        ),
    ]
