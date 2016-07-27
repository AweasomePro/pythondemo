# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0008_auto_20160725_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('trade_no', models.CharField(db_index=True, editable=False, max_length=32)),
                ('unit_price', models.IntegerField(default=1, verbose_name='单位价格(元)')),
                ('number', models.IntegerField(verbose_name='购买的数量')),
                ('total_price', models.FloatField(verbose_name='总价')),
                ('status', models.IntegerField(choices=[(1, '未支付'), (2, '支付成功')], default=1)),
                ('pay_method', models.IntegerField(choices=[(1, '支付宝')], default=1)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
