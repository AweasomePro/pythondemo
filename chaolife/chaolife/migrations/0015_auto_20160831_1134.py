# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0014_auto_20160830_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(related_name='customer_orders', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='消费者', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='order',
            name='deleted',
            field=models.BooleanField(verbose_name='删除', default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.CharField(db_index=True, primary_key=True, max_length=64, verbose_name='订单号', blank=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, related_name='product_orders', blank=True, to='chaolife.Product', verbose_name='产品', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
