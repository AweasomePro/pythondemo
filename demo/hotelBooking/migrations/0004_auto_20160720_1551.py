# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.models.counters
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0003_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', enumfields.fields.EnumIntegerField(primary_key=True, verbose_name='identifier', enum=hotelBooking.models.counters.CounterType, serialize=False)),
                ('value', models.IntegerField(default=0, verbose_name='value')),
            ],
            options={
                'verbose_name_plural': 'counters',
                'verbose_name': 'counter',
            },
        ),
        migrations.AlterField(
            model_name='pay',
            name='id',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False),
        ),
    ]
