# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_remove_roompackage_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='roompackage',
            name='extra',
            field=jsonfield.fields.JSONField(help_text='Arbitrary information for this roompackage object.', default=dict, verbose_name='Extra fields'),
        ),
    ]
