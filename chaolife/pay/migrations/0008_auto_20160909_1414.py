# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0007_invoice_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'verbose_name': '用户发票', 'verbose_name_plural': '用户发票', 'ordering': ('-modified_at', '-id')},
        ),
        migrations.AddField(
            model_name='invoice',
            name='closed',
            field=models.BooleanField(verbose_name='该发票已关闭', default=False),
        ),
    ]
