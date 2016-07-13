# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.core.exceptions


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_auto_20160712_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password', validators=[hotelBooking.core.exceptions.UserCheck.validate_pwd]),
        ),
    ]
