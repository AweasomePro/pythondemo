# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelOrderOptLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='创建的时间', editable=False)),
                ('process_state', models.IntegerField(help_text='操作后的状态')),
                ('description', models.CharField(help_text='对此次操作的描述', max_length=254)),
                ('auto_opt', models.BooleanField(default=False, help_text='表示是否是系统自动的操作')),
                ('hotelPackageOrder', models.ForeignKey(to='chaolife.HotelPackageOrder')),
            ],
        ),
    ]
