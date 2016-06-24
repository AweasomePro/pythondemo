# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0012_city_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_loggin',
            field=models.BooleanField(default=False),
        ),
    ]
