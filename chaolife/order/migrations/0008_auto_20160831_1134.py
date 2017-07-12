# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20160830_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrefund',
            name='code',
            field=models.CharField(help_text='退款编号', primary_key=True, serialize=False, max_length=32),
        ),
    ]
