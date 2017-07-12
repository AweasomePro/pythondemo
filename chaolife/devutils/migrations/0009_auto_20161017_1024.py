# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0008_apk_platform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apk',
            old_name='platform',
            new_name='client',
        ),
    ]
