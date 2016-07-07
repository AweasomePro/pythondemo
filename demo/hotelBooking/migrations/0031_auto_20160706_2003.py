# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0030_agentroomtypestate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentroomtypestate',
            name='date',
            field=models.DateField(),
        ),
    ]
