# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0004_auto_20160701_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='绑定用户'),
        ),
    ]
