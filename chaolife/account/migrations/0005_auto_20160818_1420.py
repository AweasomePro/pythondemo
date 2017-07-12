# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_pointredemption'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointredemption',
            options={'ordering': ('-modified',)},
        ),
    ]
