# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0004_auto_20160614_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelLogoImg',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('img_url', models.CharField(max_length=250)),
            ],
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='introduce_imgs',
        ),
        migrations.AddField(
            model_name='hotellogoimg',
            name='hotel',
            field=models.ForeignKey(to='hotelBooking.Hotel'),
        ),
    ]
