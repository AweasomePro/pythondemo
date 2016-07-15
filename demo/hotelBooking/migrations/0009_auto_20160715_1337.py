# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.core.exceptions


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0008_auto_20160714_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='enabled',
            new_name='active',
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.IntegerField(choices=[(1, '酒店订房')], editable=False, default=1, verbose_name='product type'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(validators=[hotelBooking.core.exceptions.UserCheck.validate_pwd], max_length=128, verbose_name='password'),
        ),
    ]
