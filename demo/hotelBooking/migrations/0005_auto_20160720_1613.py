# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0004_auto_20160720_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='trade_no',
            field=models.IntegerField(db_index=True, editable=False, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pay',
            name='id',
            field=models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID'),
        ),
    ]
