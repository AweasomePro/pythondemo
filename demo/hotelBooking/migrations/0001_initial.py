# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hotelBooking.helper.fiels
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('email', models.EmailField(max_length=255)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BigIntegerField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True)),
                ('permissions', models.ManyToManyField(to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name_plural': '用户',
                'verbose_name': '用户',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='城市字母拼音')),
                ('name_py', models.CharField(max_length=200, verbose_name='城市中文拼音')),
            ],
            options={
                'verbose_name_plural': '城市',
                'verbose_name': '城市',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='酒店名')),
                ('address', models.CharField(max_length=255)),
                ('introduce', models.CharField(max_length=255)),
                ('contact_phone', models.CharField(max_length=255)),
                ('city', models.ForeignKey(to='hotelBooking.City', verbose_name='所在城市', related_name='hotels')),
            ],
            options={
                'verbose_name_plural': '酒店',
                'verbose_name': '酒店',
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', verbose_name='所属酒店', related_name='houses')),
            ],
            options={
                'verbose_name_plural': '房源',
                'verbose_name': '房源',
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('badge', models.BigIntegerField(null=True, default=0, verbose_name='ios badge数')),
                ('channels', hotelBooking.helper.fiels.ListField(default=[], verbose_name='订阅渠道')),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('deviceToken', models.CharField(max_length=200, null=True, unique=True)),
                ('deviceType', models.CharField(max_length=200, default='')),
                ('installationId', models.CharField(null=True, max_length=200, verbose_name='设备id', unique=True)),
                ('timeZone', models.CharField(max_length=200, default='', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=-1, verbose_name='绑定用户', null=True)),
            ],
            options={
                'verbose_name_plural': '设备',
                'verbose_name': 'App已安装设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('test_list', hotelBooking.helper.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('name_py', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': '省份',
                'verbose_name': '省份',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='hotelBooking.Province', verbose_name='所属省份', related_name='citys'),
        ),
    ]
