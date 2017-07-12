# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0002_auto_20160822_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='platform',
            field=models.SmallIntegerField(blank=True, default=1, choices=[(1, 'android'), (2, 'ios')]),
            preserve_default=False,
        ),
    ]
