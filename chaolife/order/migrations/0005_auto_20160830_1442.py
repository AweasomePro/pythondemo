# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_orderbill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbill',
            name='settled_at',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, when=set([True]), monitor='settled'),
        ),
    ]
