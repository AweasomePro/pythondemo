# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0004_auto_20160822_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='platform',
            new_name='client_type',
        ),
    ]
