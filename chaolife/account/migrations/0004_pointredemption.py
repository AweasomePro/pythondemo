# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160811_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointRedemption',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('state', models.IntegerField()),
                ('points', models.PositiveIntegerField(verbose_name='提现积分')),
                ('card', models.CharField(verbose_name='提现卡号', max_length=40)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
