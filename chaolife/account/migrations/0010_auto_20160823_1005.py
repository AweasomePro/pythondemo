# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20160822_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermember',
            name='profile_integrity',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_integrity',
            field=models.BooleanField(default=False),
        ),
    ]
