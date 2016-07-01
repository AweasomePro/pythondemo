# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_producttype_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'orders', 'ordering': ('created_on',), 'verbose_name': 'order'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': '产品（数据库基类）', 'ordering': ('-id',), 'verbose_name': '产品（数据库基类）'},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'verbose_name_plural': '产品类型', 'verbose_name': '产品类型'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AddField(
            model_name='order',
            name='number',
            field=models.CharField(blank=True, unique=True, db_index=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False),
        ),
        migrations.AlterField(
            model_name='hotelimg',
            name='hotel',
            field=models.ForeignKey(verbose_name='房型', to='hotelBooking.Hotel', related_name='house_imgs'),
        ),
        migrations.AlterField(
            model_name='houseimg',
            name='house',
            field=models.ForeignKey(verbose_name='房型', to='hotelBooking.House', related_name='house_imgs'),
        ),
        migrations.AlterField(
            model_name='installation',
            name='deviceToken',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.ForeignKey(to='hotelBooking.ProductType', verbose_name='product type'),
        ),
    ]
