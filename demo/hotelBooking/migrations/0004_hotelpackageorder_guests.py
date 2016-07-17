# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0003_roompackage_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpackageorder',
            name='guests',
            field=jsonfield.fields.JSONField(help_text='入住人信息', blank=True, null=True),
        ),
    ]
