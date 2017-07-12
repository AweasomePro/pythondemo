# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20160823_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermember',
            name='point',
        ),
        migrations.AddField(
            model_name='customermember',
            name='points',
            field=models.PositiveIntegerField(verbose_name='积分', editable=False, default=0),
        ),
    ]
