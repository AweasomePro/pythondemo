# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20160823_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customermember',
            old_name='point',
            new_name='points',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='point',
            new_name='points',
        ),
    ]
