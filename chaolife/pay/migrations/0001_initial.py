# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import common.fiels
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('value', common.fiels.PositiveFloatField(verbose_name='开票金额')),
                ('title', models.CharField(help_text='发票抬头', max_length=255, verbose_name='发票抬头')),
                ('phone_number', models.CharField(help_text='联系方式_手机号', max_length=20, verbose_name='联系方式')),
                ('recipient_name', models.CharField(help_text='收件人姓名', max_length=254, verbose_name='收件人名字')),
                ('recipient_address', models.CharField(help_text='邮寄地址', max_length=254, verbose_name='邮寄地址')),
                ('checked', models.BooleanField(verbose_name='审查通过', default=False)),
                ('mailed', models.BooleanField(help_text='是否已经邮寄', verbose_name='已经邮寄?', default=False)),
                ('user', models.ForeignKey(to_field='phone_number', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PointPay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('trade_no', models.CharField(editable=False, max_length=32, db_index=True)),
                ('unit_price', models.PositiveIntegerField(verbose_name='单位价格(元)', default=1)),
                ('number', models.PositiveIntegerField(verbose_name='购买的数量')),
                ('total_price', models.FloatField(help_text='交易总价', verbose_name='总价')),
                ('status', models.IntegerField(help_text='表示是否支付成功，需要第三方服务回调才能确认', default=0, choices=[(0, '未支付'), (1, '支付成功')])),
                ('pay_method', models.IntegerField(help_text='支付渠道', default=1, choices=[(1, '支付宝')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
