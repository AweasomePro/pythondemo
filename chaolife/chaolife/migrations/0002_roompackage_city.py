# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roompackage',
            name='city',
            field=models.ForeignKey(default=3, to='chaolife.City', verbose_name='城市', help_text='所属城市'),
            preserve_default=False,
        ),
    ]
