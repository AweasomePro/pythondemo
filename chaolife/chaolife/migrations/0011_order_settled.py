# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0010_remove_hotelpackageorder_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='settled',
            field=models.BooleanField(default=False, help_text='是否已结算', verbose_name='已结算?'),
        ),
    ]
