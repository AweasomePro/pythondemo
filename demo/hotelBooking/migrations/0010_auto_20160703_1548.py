# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0009_auto_20160703_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.IntegerField(db_index=True, choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')], default=1, verbose_name='payment status'),
        ),
    ]
