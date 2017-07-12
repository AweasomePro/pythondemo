# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0006_apk_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apk',
            name='url',
            field=models.URLField(verbose_name='url', null=True, blank=True),
        ),
    ]
