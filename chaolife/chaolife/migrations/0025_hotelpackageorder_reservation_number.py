# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0024_hotelpackageorder_price_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpackageorder',
            name='reservation_number',
            field=models.CharField(verbose_name='预订号', max_length=20, help_text='酒店预订号', blank=True),
        ),
    ]
