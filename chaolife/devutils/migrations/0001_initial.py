# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('apk', models.FileField(upload_to='')),
                ('version', models.CharField(max_length=255, verbose_name='版本号')),
                ('type', models.CharField(choices=[('ios', '苹果'), ('android', '安卓')], max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
