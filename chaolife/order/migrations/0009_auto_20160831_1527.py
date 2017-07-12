# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20160831_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrefund',
            name='detail_state',
            field=models.IntegerField(blank=True, default=0, verbose_name='详细状态'),
        ),
        migrations.AlterField(
            model_name='orderrefund',
            name='state',
            field=models.IntegerField(choices=[(1, '申请中'), (2, '接收退货(款)'), (-1, '拒绝退货(款)'), (1, '退货完成')], verbose_name='申请状态'),
        ),
        migrations.AlterField(
            model_name='orderrefund',
            name='success_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='退款成功时间'),
        ),
    ]
