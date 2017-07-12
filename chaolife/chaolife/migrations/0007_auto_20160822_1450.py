# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0006_auto_20160822_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(verbose_name='已上线 ?', default=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='active',
            field=models.BooleanField(verbose_name='已上线 ?', default=False),
        ),
    ]
