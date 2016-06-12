# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hotelBooking.helper.fiels


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_auto_20160607_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('badge', models.BigIntegerField()),
                ('channels', hotelBooking.helper.fiels.ListField()),
                ('deviceProfile', models.CharField(max_length=200)),
                ('deviceToken', models.CharField(max_length=200, unique=True)),
                ('deviceType', models.CharField(max_length=200)),
                ('installationId', models.CharField(max_length=200, unique=True)),
                ('timeZone', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('test_list', hotelBooking.helper.fiels.ListField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='member',
            managers=[
            ],
        ),
    ]
