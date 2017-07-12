# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20160819_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointredemption',
            name='email',
        ),
        migrations.AddField(
            model_name='pointredemption',
            name='card',
            field=models.CharField(default=12323121321, max_length=40, verbose_name='提现卡号'),
            preserve_default=False,
        ),
    ]
