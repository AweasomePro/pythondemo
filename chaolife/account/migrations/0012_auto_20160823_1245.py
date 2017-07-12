# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import account.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20160823_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermember',
            name='consumptions',
            field=models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='消费金额'),
        ),
        migrations.AddField(
            model_name='customermember',
            name='invoiced_consumptions',
            field=models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='已开票金额'),
        ),
        migrations.AddField(
            model_name='customermember',
            name='point',
            field=account.models.fields.PointField(default=0, editable=False, verbose_name='积分'),
        ),
    ]
