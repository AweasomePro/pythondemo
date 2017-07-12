# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0004_auto_20161012_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apk',
            name='des',
            field=models.TextField(default='版本描述', verbose_name='版本更新详情', max_length=500),
        ),
        migrations.AlterField(
            model_name='apk',
            name='version_name',
            field=models.CharField(default='versionName', verbose_name='versionName', max_length=255),
        ),
    ]
