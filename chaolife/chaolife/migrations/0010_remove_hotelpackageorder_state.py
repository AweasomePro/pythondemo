# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0009_auto_20160830_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelpackageorder',
            name='state',
        ),
    ]
