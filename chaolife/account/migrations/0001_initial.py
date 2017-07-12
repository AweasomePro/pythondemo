# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import account.models.fields
import django.utils.timezone
import common.fiels
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20160712_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('point', account.models.fields.PointField(editable=False, verbose_name='积分', default=0)),
                ('consumptions', models.PositiveIntegerField(verbose_name='消费金额', blank=True, default=0, null=True)),
                ('invoiced_consumptions', models.PositiveIntegerField(verbose_name='已开票金额', blank=True, default=0, null=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('pay_pwd', models.CharField(max_length=6, verbose_name='password', default='000000')),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('sex', models.IntegerField(default=1, choices=[(1, 'male'), (0, 'female')])),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_login', models.BooleanField(default=False)),
                ('role', models.IntegerField(help_text='该账号的角色标识', default=1, choices=[(1, '顾客'), (2, '酒店代理合作伙伴')])),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='BillHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('type', models.IntegerField(choices=[(1, '积分充值'), (2, '酒店预订'), (3, '酒店资源销售'), (4, '积分提现'), (5, '酒店预订取消,积分退还')])),
                ('gains', models.SmallIntegerField(help_text='获得或者扣除的积分')),
                ('business_id', models.CharField(help_text='对应的业务主键id', max_length=64)),
                ('description', models.CharField(help_text='简短的业务描述，如（积分充值，酒店预订-北京-xx酒店）', max_length=255)),
            ],
            options={
                'ordering': ('-modified',),
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=200, default=django.utils.timezone.now)),
                ('channels', common.fiels.ListField(verbose_name='订阅渠道', default=['public', 'private'], null=True)),
                ('deviceToken', models.CharField(max_length=200, null=True)),
                ('installationId', models.CharField(max_length=200, verbose_name='设备id', null=True)),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('active', models.BooleanField(verbose_name='active?', default=True)),
            ],
            options={
                'verbose_name': 'App已安装设备',
                'verbose_name_plural': '设备',
            },
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('avatar', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': '会员',
                'verbose_name_plural': '会员',
            },
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': '加盟会员',
                'verbose_name_plural': '加盟会员',
            },
        ),
        migrations.AddField(
            model_name='installation',
            name='user',
            field=models.ForeignKey(to_field='phone_number', to=settings.AUTH_USER_MODEL, verbose_name='绑定用户', null=True),
        ),
        migrations.AddField(
            model_name='billhistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='主体'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_name='user_set', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', blank=True, related_name='user_set', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
