# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0007_housepackage_checked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='types',
        ),
        migrations.AddField(
            model_name='house',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='审核过 ?'),
        ),
        migrations.AddField(
            model_name='house',
            name='enabled',
            field=models.BooleanField(default=False, verbose_name='是否可用 ?'),
        ),
        migrations.AlterField(
            model_name='housepackage',
            name='detail',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='RoomType',
        ),
    ]
