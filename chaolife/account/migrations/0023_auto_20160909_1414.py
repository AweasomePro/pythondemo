# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_auto_20160901_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointredemption',
            options={'verbose_name': '提现申请', 'verbose_name_plural': '提现申请', 'ordering': ('-modified_at',)},
        ),
        migrations.AlterField(
            model_name='partnermember',
            name='invoice',
            field=models.PositiveIntegerField(verbose_name='可开积分余额', help_text='客户向我方邮寄的发票转换的可开积分余额', default=0),
        ),
    ]
