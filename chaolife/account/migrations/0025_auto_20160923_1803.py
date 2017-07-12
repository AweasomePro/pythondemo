# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_inviterecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inviterecord',
            name='inviter_reward_points',
            field=models.IntegerField(verbose_name='邀请用户奖励积分', default=0),
        ),
        migrations.AlterField(
            model_name='inviterecord',
            name='recharge_point_amount',
            field=models.IntegerField(verbose_name='被邀请者充值数量', default=0),
        ),
    ]
