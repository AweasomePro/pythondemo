# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0020_splashimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splashimg',
            name='version',
            field=models.CharField(max_length=10, unique=True, default=0.1, verbose_name='版本'),
        ),
    ]
