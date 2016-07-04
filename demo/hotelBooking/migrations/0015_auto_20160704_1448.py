# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0014_auto_20160704_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelpackageorder',
            name='extra_message',
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='comment',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='require_notes',
            field=models.TextField(null=True, blank=True),
        ),

        migrations.AddField(
            model_name='order',
            name='franchisee',
            field=models.ForeignKey(related_name='franchisee_orders', blank=True, default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default='M', choices=[('M', 'male'), ('F', 'female')], max_length=10),
        ),
        migrations.AlterField(
            model_name='hotelimg',
            name='hotel',
            field=models.ForeignKey(related_name='hotel_imgs', to='hotelBooking.Hotel', verbose_name='房型'),
        ),
        migrations.AlterField(
            model_name='hotelpackageorder',
            name='process_state',
            field=models.IntegerField(default=1, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (16, '代理接收了订单'), (32, '代理拒绝了订单'), (48, '代理提前表示某些原因导致不能入住了')], help_text='订单进行的状态'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_orders', blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='customer'),
        ),
    ]
