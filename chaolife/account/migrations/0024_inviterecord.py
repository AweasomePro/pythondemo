# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_auto_20160909_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('recharged', models.BooleanField(verbose_name='已充值', default=False, help_text='被邀请者是否已充值')),
                ('recharge_point_amount', models.IntegerField(verbose_name='被邀请者充值数量')),
                ('inviter_reward_points', models.IntegerField(verbose_name='邀请用户奖励积分')),
                ('recharge_time', models.DateTimeField(blank=True, help_text='首次充值的时间')),
                ('invitee', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='inviteeRecord')),
                ('inviter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
