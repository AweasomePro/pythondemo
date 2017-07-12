# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0005_auto_20160822_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='reject_reason',
            field=models.CharField(help_text='拒绝原因', blank=True, max_length=50, verbose_name='拒绝原因'),
        ),
    ]
