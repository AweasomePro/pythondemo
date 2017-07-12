# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devutils', '0002_auto_20161011_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apk',
            options={'ordering': ('type', '-version')},
        ),
    ]
