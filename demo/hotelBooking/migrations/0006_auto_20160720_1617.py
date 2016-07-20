# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0005_auto_20160720_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='trade_no',
            field=models.CharField(max_length=32, editable=False, db_index=True),
        ),
    ]
