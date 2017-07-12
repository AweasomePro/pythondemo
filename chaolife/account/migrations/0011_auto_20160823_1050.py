# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20160823_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billhistory',
            name='gains',
            field=models.IntegerField(help_text='获得或者扣除的积分'),
        ),
    ]
