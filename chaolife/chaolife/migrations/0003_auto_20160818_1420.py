# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chaolife', '0002_roompackage_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelpackageorder',
            options={'verbose_name': '酒店订单', 'permissions': (('change_process_state', '能够操作改变订单过程状态'),), 'ordering': ('-process_state_change_at',), 'verbose_name_plural': '酒店订单'},
        ),
        migrations.AddField(
            model_name='hotel',
            name='brief_address',
            field=models.CharField(verbose_name='简单的地址描述', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(db_index=True, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了'), (-100, '代理超时确认，自动取消'), (20, '客户入住中(ing)'), (30, '到达ckeckoutTime之后'), (40, '交易积分已转到代理商账号')], default=1, help_text='订单进行的状态'),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='success',
            field=models.BooleanField(default=False, help_text='订单完成'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(verbose_name='customer', blank=True, related_name='customer_orders', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, editable=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(verbose_name='modifier user', blank=True, related_name='orders_modified', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, editable=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(verbose_name='product', blank=True, related_name='product_orders', null=True, to='chaolife.Product', on_delete=django.db.models.deletion.SET_NULL, editable=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(related_name='seller_orders', blank=True, default=1000, to=settings.AUTH_USER_MODEL, editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='checked',
            field=models.BooleanField(verbose_name='审核通过', default=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='checked',
            field=models.BooleanField(verbose_name='审核通过', default=True),
        ),
    ]
