# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20160818_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointRedemptionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='pointredemption',
            name='card',
        ),
        migrations.AddField(
            model_name='pointredemption',
            name='email',
            field=models.EmailField(verbose_name='发票邮寄地址', default=1, max_length=254),
            preserve_default=False,
        ),
    ]
