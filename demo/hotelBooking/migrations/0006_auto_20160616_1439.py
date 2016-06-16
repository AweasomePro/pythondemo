# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0005_auto_20160616_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='HousePackage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('package_name', models.CharField(verbose_name='套餐名', max_length=255, default='套餐名')),
                ('need_point', models.IntegerField(verbose_name='所需积分')),
                ('package_state', models.CharField(choices=[(0, '充沛'), (1, '满房')], max_length=255)),
                ('detail', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='hotellogoimg',
            options={'verbose_name_plural': '酒店展示图片', 'verbose_name': '酒店展示图片'},
        ),
        migrations.AlterModelOptions(
            name='house',
            options={'verbose_name_plural': '房型', 'verbose_name': '房型'},
        ),
        migrations.AddField(
            model_name='house',
            name='name',
            field=models.CharField(verbose_name='房型', max_length=255, default='未定义'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(verbose_name='地址', max_length=255),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='contact_phone',
            field=models.CharField(verbose_name='联系电话', max_length=255),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='introduce',
            field=models.TextField(verbose_name='介绍', max_length=255),
        ),
        migrations.AlterField(
            model_name='hotellogoimg',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hotellogoimg',
            name='img_url',
            field=models.CharField(verbose_name='图片地址', max_length=250),
        ),
        migrations.AddField(
            model_name='housepackage',
            name='house',
            field=models.ForeignKey(verbose_name='房型', to='hotelBooking.House'),
        ),
        migrations.AddField(
            model_name='houseimg',
            name='house',
            field=models.ForeignKey(verbose_name='房型', to='hotelBooking.House'),
        ),
    ]
