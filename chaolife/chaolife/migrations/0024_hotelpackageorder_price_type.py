# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0023_auto_20160928_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpackageorder',
            name='price_type',
            field=models.IntegerField(help_text='单人价格|双人价格', default=1),
        ),
    ]
