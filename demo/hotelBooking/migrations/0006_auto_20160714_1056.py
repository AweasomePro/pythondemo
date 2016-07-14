# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0005_auto_20160713_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, default='商务大床房')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '所有房型',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='types',
            field=models.ManyToManyField(to='hotelBooking.RoomType'),
        ),
    ]
