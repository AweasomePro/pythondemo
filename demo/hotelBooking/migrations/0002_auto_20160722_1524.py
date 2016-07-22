# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'order', 'ordering': ('modified',), 'verbose_name_plural': 'orders'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='order',
            name='modified_on',
        ),
        migrations.AddField(
            model_name='order',
            name='created',
            field=model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='order',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.CharField(db_index=True, unique=True, max_length=64, editable=False, serialize=False, primary_key=True, blank=True),
        ),
    ]
