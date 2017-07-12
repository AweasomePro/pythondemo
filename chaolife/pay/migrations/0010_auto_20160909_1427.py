# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0009_auto_20160909_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='closed',
            new_name='viewed',
        ),
    ]
