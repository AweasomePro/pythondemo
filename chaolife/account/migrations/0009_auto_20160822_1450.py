# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20160819_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointredemption',
            options={'ordering': ('-modified_at',)},
        ),
        migrations.RenameField(
            model_name='pointredemption',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='pointredemption',
            old_name='modified',
            new_name='modified_at',
        ),
    ]
