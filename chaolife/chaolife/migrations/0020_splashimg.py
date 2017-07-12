# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0019_auto_20160922_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplashImg',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img', models.ImageField(upload_to='', verbose_name='图片')),
                ('version', models.CharField(max_length=10, default=0.1, verbose_name='版本')),
                ('active', models.BooleanField(default=False, verbose_name='是否在前端显示')),
            ],
            options={
                'verbose_name': '闪屏图',
            },
        ),
    ]
