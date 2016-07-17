# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0004_hotelpackageorder_guests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roompackage',
            name='extra',
            field=jsonfield.fields.JSONField(null=True, verbose_name='Extra fields', help_text='Arbitrary information for this roompackage object.', blank=True),
        ),
    ]
