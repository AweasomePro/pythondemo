# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0003_auto_20160818_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='customer_orders', verbose_name='customer', on_delete=django.db.models.deletion.PROTECT, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.CharField(db_index=True, serialize=False, max_length=64, primary_key=True, unique=True, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='chaolife.Product', null=True, related_name='product_orders', verbose_name='product', on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(default=1000, related_name='seller_orders', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
