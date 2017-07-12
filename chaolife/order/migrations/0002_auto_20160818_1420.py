# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelorderoptlog',
            name='auto_opt',
            field=models.BooleanField(default=False, help_text='表示是否是系统自动的操作', editable=False),
        ),
        migrations.AlterField(
            model_name='hotelorderoptlog',
            name='process_state',
            field=models.IntegerField(help_text='操作后的状态', editable=False),
        ),
    ]
