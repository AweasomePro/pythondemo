# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_token_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='platform',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'client'), (2, 'business')]),
        ),
    ]
