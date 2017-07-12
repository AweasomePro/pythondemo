# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0021_auto_20160926_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareNotify',
            fields=[
                ('name', models.CharField(verbose_name='分享的主题', primary_key=True, serialize=False, max_length=100)),
                ('title', models.CharField(verbose_name='标题', max_length=50)),
                ('sub_title', models.CharField(blank=True, verbose_name='副标题', max_length=50, null=True)),
                ('content', models.TextField(blank=True, verbose_name='内容', max_length=500, null=True)),
                ('extra_link', models.URLField(blank=True, verbose_name='链接', null=True)),
            ],
            options={
                'verbose_name': '活动通知',
                'verbose_name_plural': '活动通知',
            },
        ),
    ]
