# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apk',
            options={'ordering': ('type', 'version')},
        ),
        migrations.AlterField(
            model_name='apk',
            name='version',
            field=models.FloatField(max_length=255, verbose_name='版本号'),
        ),
    ]
