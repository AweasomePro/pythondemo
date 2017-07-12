# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0008_auto_20160909_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='state',
            field=models.IntegerField(choices=[(1, '申请发票'), (2, '发票请求申请成功'), (-1, '发票请求拒绝'), (3, '发票邮寄成功')]),
        ),
        migrations.AlterField(
            model_name='invoicetimeline',
            name='state',
            field=models.IntegerField(choices=[(1, '申请发票'), (2, '发票请求申请成功'), (-1, '发票请求拒绝'), (3, '发票邮寄成功')]),
        ),
    ]
