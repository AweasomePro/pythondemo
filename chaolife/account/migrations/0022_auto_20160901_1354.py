# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20160831_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnermember',
            name='deposit_points',
            field=models.IntegerField(default=0, verbose_name='押金积分'),
        ),
        migrations.AlterField(
            model_name='billhistory',
            name='type',
            field=models.IntegerField(choices=[(1, '积分充值'), (2, '酒店预订'), (3, '酒店资源销售'), (6, '酒店订单赔付'), (4, '积分提现'), (5, '酒店预订取消,积分退还'), (301, '邀请用户,奖励积分')]),
        ),
    ]
