# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceTimeLine',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('state', models.IntegerField(choices=[(1, '申请发票'), (2, '发票请求申请成功'), (3, '发票邮寄成功'), (-1, '发票请求拒绝')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='created',
            new_name='create_at',
        ),
        migrations.RenameField(
            model_name='pointpay',
            old_name='created',
            new_name='create_at',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='checked',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='mailed',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='recipient_address',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='recipient_name',
        ),
        migrations.AddField(
            model_name='invoice',
            name='email',
            field=models.EmailField(verbose_name='邮寄地址', max_length=254, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='state',
            field=models.IntegerField(choices=[(1, '申请发票'), (2, '发票请求申请成功'), (3, '发票邮寄成功'), (-1, '发票请求拒绝')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoicetimeline',
            name='invoice',
            field=models.ForeignKey(to='pay.Invoice'),
        ),
    ]
