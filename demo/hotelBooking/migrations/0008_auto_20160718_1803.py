# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0007_auto_20160718_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('unit_price', models.IntegerField(default=1, verbose_name='单位价格(元)')),
                ('number', models.IntegerField(verbose_name='购买的数量')),
                ('total_price', models.FloatField(verbose_name='总价')),
                ('status', models.IntegerField(default=1, choices=[(1, '未支付'), (2, '支付成功')])),
                ('pay_method', models.IntegerField(default=1, choices=[(1, '支付宝')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 18, 3, 25, 30431), auto_now_add=True, verbose_name='State modified'),
            preserve_default=False,
        ),
    ]
