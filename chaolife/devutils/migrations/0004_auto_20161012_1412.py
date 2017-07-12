# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0003_auto_20161011_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='apk',
            name='des',
            field=models.TextField(verbose_name='版本更新详情', max_length=500, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apk',
            name='version_name',
            field=models.CharField(verbose_name='versionName', max_length=255, default=1),
            preserve_default=False,
        ),
    ]
