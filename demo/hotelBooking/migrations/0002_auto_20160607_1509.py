# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phoneNumber',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='member',
            name='registerTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
