# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0008_auto_20160721_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermember',
            name='id',
        ),
        migrations.RemoveField(
            model_name='partnermember',
            name='id',
        ),
        migrations.RemoveField(
            model_name='partnermember',
            name='type',
        ),
        migrations.AlterField(
            model_name='customermember',
            name='user',
            field=models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True),
        ),
        migrations.AlterField(
            model_name='partnermember',
            name='user',
            field=models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True),
        ),
    ]
