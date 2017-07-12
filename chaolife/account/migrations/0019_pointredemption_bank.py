# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_partnermember_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointredemption',
            name='bank',
            field=models.CharField(verbose_name='提现所属银行', max_length=40, default=1),
            preserve_default=False,
        ),
    ]
