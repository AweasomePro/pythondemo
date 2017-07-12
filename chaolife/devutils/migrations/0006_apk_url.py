# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0005_auto_20161012_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='apk',
            name='url',
            field=models.URLField(default=1, verbose_name='url'),
            preserve_default=False,
        ),
    ]
