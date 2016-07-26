# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0009_hotelordernumbergenerator_pay_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='agent',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),

    ]
