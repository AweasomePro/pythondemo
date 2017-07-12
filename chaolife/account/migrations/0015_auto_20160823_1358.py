# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import account.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20160823_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermember',
            name='points',
        ),
        migrations.AddField(
            model_name='customermember',
            name='point',
            field=account.models.fields.PointField(default=0, verbose_name='积分'),
        ),
    ]
