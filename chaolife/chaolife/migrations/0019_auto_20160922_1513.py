# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0018_auto_20160909_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': '城市', 'verbose_name_plural': '城市', 'ordering': ('-hot', 'name')},
        ),
    ]
