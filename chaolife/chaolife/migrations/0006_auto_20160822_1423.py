# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0005_hotel_established_des'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(verbose_name='已上线 ?', default=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='active',
            field=models.BooleanField(verbose_name='已上线 ?', default=True),
        ),
    ]
