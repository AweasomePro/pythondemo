# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0003_auto_20160822_1423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-modified_at',)},
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='create_at',
        ),
        migrations.AddField(
            model_name='invoice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 22, 14, 49, 56, 530221)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 8, 22, 14, 50, 2, 384072)),
            preserve_default=False,
        ),
    ]
