# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0005_auto_20160823_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={'ordering': ('user', '-created')},
        ),
    ]
