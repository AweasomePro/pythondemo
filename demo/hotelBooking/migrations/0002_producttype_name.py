# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='name',
            field=models.CharField(verbose_name='name', max_length=64, default=1),
            preserve_default=False,
        ),
    ]
