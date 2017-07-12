# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0007_auto_20161013_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='apk',
            name='platform',
            field=models.IntegerField(choices=[(0, '客户端'), (1, '商家端')], default=0, verbose_name='platform 商家端(1) or 客户端(0)'),
        ),
    ]
