# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0004_auto_20160819_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='established_des',
            field=models.CharField(verbose_name='开业时间描述', blank=True, max_length=50),
        ),
    ]
