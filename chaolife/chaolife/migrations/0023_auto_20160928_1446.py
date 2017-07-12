# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0022_sharenotify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharenotify',
            name='extra_link',
        ),
        migrations.AddField(
            model_name='sharenotify',
            name='extra_image',
            field=models.ImageField(verbose_name='图片', null=True, blank=True, upload_to=''),
        ),
    ]
