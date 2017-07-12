# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import account.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20160823_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnermember',
            name='points',
            field=models.PositiveIntegerField(default=0, verbose_name='积分'),
        ),
        migrations.AlterField(
            model_name='user',
            name='point',
            field=account.models.fields.PointField(default=0, verbose_name='积分'),
        ),
    ]
