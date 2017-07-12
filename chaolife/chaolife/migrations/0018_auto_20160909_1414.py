# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0017_auto_20160901_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelpackageorderitem',
            options={'ordering': ('order', '-day')},
        ),
    ]
