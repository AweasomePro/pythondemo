# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20160823_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='consumptions',
        ),
        migrations.RemoveField(
            model_name='user',
            name='invoiced_consumptions',
        ),
        migrations.RemoveField(
            model_name='user',
            name='points',
        ),
    ]
