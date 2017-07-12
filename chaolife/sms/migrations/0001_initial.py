# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('business_id', models.UUIDField(help_text='前端发送过来验证的唯一标识')),
                ('phone_number', models.CharField(max_length=20, help_text='发送的手机号')),
                ('state', models.IntegerField(choices=[(1, '发送成功'), (-1, '发送失败'), (2, '等待验证'), (3, '验证成功')])),
                ('vertify_code', models.CharField(max_length=10, verbose_name='验证码')),
                ('ali_code', models.IntegerField(help_text='阿里返回的code')),
                ('ali_template_code', models.CharField(max_length=100, help_text='发送时的短信模板')),
                ('ali_sub_code', models.CharField(max_length=100, help_text='阿里返回的sub_code')),
                ('ali_sub_msg', models.CharField(max_length=100, help_text='阿里返回的sub_msg')),
                ('user', models.ForeignKey(help_text='发送给的用户', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
    ]
