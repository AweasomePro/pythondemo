# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import hotelBooking.core.models.products


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=enumfields.fields.EnumIntegerField(enum=hotelBooking.core.models.products.ProductTypeEnum, default=0, verbose_name='product type'),
        ),
        migrations.DeleteModel(
            name='ProductType',
        ),
    ]
