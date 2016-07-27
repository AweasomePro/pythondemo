# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0003_hotel_smoking'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelimg',
            name='img',
            field=models.ImageField(upload_to='', verbose_name='图片', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roomimg',
            name='img',
            field=models.ImageField(upload_to='', verbose_name='图片', default=1),
            preserve_default=False,
        ),
    ]
