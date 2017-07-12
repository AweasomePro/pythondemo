# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0006_invoice_reject_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='type',
            field=models.IntegerField(choices=[(1, '代订房费'), (2, '旅游服务费'), (3, '服务费')], default=1),
            preserve_default=False,
        ),
    ]
