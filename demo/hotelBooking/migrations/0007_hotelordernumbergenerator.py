# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0006_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
    ]
