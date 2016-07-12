# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housepackage',
            name='breakfast',
            field=models.IntegerField(verbose_name='早餐类型', choices=[(1, '无早'), (2, '单早'), (3, '双早')], default=1),
        ),
    ]
