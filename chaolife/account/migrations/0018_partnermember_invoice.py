# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20160823_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnermember',
            name='invoice',
            field=models.PositiveIntegerField(verbose_name='收到的发票', help_text='客户向我方邮寄的发票', default=0),
        ),
    ]
