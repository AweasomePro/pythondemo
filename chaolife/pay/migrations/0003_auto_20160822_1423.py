# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0002_auto_20160819_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='state',
            field=models.IntegerField(choices=[(1, '申请发票'), (2, '发票请求申请成功'), (-1, '发票请求拒绝'), (3, '发票邮寄成功'), (4, '发票完成')]),
        ),
        migrations.AlterField(
            model_name='invoicetimeline',
            name='state',
            field=models.IntegerField(choices=[(1, '申请发票'), (2, '发票请求申请成功'), (-1, '发票请求拒绝'), (3, '发票邮寄成功'), (4, '发票完成')]),
        ),
    ]
