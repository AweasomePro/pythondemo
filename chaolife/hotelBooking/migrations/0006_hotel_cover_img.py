# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0005_auto_20160724_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='cover_img',
            field=models.ImageField(default=1, verbose_name='封面图片', upload_to=''),
            preserve_default=False,
        ),
    ]
