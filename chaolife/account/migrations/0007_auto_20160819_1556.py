# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20160819_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointredemptionlog',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='pointredemptionlog',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 19, 15, 56, 51, 326543), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pointredemptionlog',
            name='point_redemption',
            field=models.ForeignKey(default=1, to='account.PointRedemption'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pointredemptionlog',
            name='state',
            field=models.IntegerField(default=1, choices=[(1, '申请提现'), (2, '提现请求申请成功'), (3, '提现成功'), (-1, '请求拒绝')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pointredemption',
            name='state',
            field=models.IntegerField(choices=[(1, '申请提现'), (2, '提现请求申请成功'), (3, '提现成功'), (-1, '请求拒绝')]),
        ),
    ]
