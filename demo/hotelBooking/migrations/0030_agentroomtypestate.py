# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0029_auto_20160706_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentRoomTypeState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateField(unique=True)),
                ('state', models.IntegerField(default=1, choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')])),
                ('agent', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('housePackage', models.ForeignKey(to='hotelBooking.HousePackage')),
                ('house_type', models.ForeignKey(to='hotelBooking.House')),
            ],
            options={
                'verbose_name': '房间类型状态',
                'verbose_name_plural': '房间类型状态',
            },
        ),
    ]
