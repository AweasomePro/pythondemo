# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.core.models.user
import django.db.models.deletion
import hotelBooking.core.models.products
import enumfields.fields
import hotelBooking.core.fields
import hotelBooking.core.models.orders
from django.conf import settings
import hotelBooking.utils.fiels


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(default='unknow name', max_length=225)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, default=None, to='auth.Group')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission')),
            ],
            options={
                'verbose_name_plural': '用户',
                'verbose_name': '用户',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.IntegerField(verbose_name='城市代号', unique=True)),
                ('name', models.CharField(verbose_name='城市', max_length=200)),
                ('name_py', models.CharField(verbose_name='城市拼音', max_length=200)),
                ('logo', models.URLField(default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg', verbose_name='城市Logo图')),
            ],
            options={
                'verbose_name_plural': '城市',
                'verbose_name': '城市',
            },
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('avatar', models.URLField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '会员',
                'verbose_name': '会员',
            },
        ),
        migrations.CreateModel(
            name='FranchiseeMember',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('type', enumfields.fields.EnumIntegerField(verbose_name='加盟商类型', default=1, enum=hotelBooking.core.models.user.ProductMemberType)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '加盟会员',
                'verbose_name': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='酒店名', max_length=200)),
                ('address', models.CharField(verbose_name='地址', max_length=255)),
                ('introduce', models.TextField(verbose_name='介绍', max_length=255)),
                ('contact_phone', models.CharField(verbose_name='联系电话', max_length=255)),
                ('city', models.ForeignKey(related_name='hotels', verbose_name='所在城市', to='hotelBooking.City')),
            ],
            options={
                'verbose_name_plural': '酒店',
                'verbose_name': '酒店',
            },
        ),
        migrations.CreateModel(
            name='HotelImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('hotel', models.ForeignKey(related_name='house_Imgs', verbose_name='房型', to='hotelBooking.Hotel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='未定义房型名', verbose_name='房型', max_length=255)),
                ('hotel', models.ForeignKey(related_name='hotel_houses', verbose_name='所属酒店', to='hotelBooking.Hotel')),
            ],
            options={
                'verbose_name_plural': '房型',
                'verbose_name': '房型',
            },
        ),
        migrations.CreateModel(
            name='HouseImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('house', models.ForeignKey(related_name='house_Imgs', verbose_name='房型', to='hotelBooking.House')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousePackage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('package_name', models.CharField(default='套餐名', verbose_name='套餐名', max_length=255)),
                ('need_point', models.IntegerField(verbose_name='所需积分')),
                ('package_state', models.CharField(default='充沛', max_length=255, choices=[('1', '充沛'), ('2', '满房')])),
                ('detail', models.TextField()),
                ('house', models.ForeignKey(related_name='housePackages', verbose_name='房型', to='hotelBooking.House')),
                ('owner', models.ForeignKey(to='hotelBooking.FranchiseeMember')),
            ],
            options={
                'verbose_name_plural': '套餐',
                'verbose_name': '套餐',
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0, null=True)),
                ('channels', hotelBooking.utils.fiels.ListField(verbose_name='订阅渠道', default=[])),
                ('deviceProfile', models.CharField(default='', max_length=200)),
                ('deviceToken', models.CharField(max_length=200, unique=True, null=True)),
                ('deviceType', models.CharField(default='', max_length=200)),
                ('installationId', models.CharField(verbose_name='设备id', max_length=200, unique=True, null=True)),
                ('timeZone', models.CharField(default='', max_length=200, null=True)),
                ('user', models.ForeignKey(default=-1, null=True, verbose_name='绑定用户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '设备',
                'verbose_name': 'App已安装设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
                ('identifier', hotelBooking.core.fields.InternalIdentifierField(blank=True, unique=True, editable=False, db_index=True, max_length=64, null=True)),
                ('label', models.CharField(verbose_name='label', db_index=True, max_length=32)),
                ('key', models.CharField(verbose_name='key', max_length=32, unique=True)),
                ('reference_number', models.CharField(verbose_name='reference number', blank=True, unique=True, null=True, db_index=True, max_length=64)),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False)),
                ('payment_status', enumfields.fields.EnumIntegerField(verbose_name='payment status', db_index=True, default=0, enum=hotelBooking.core.models.orders.PaymentStatus)),
                ('shipping_status', enumfields.fields.EnumIntegerField(verbose_name='shipping status', db_index=True, default=0, enum=hotelBooking.core.models.orders.ShippingStatus)),
                ('customer', models.ForeignKey(related_name='customer_orders', blank=True, null=True, verbose_name='customer', to='hotelBooking.CustomerMember', on_delete=django.db.models.deletion.PROTECT)),
                ('modified_by', models.ForeignKey(related_name='orders_modified', blank=True, null=True, verbose_name='modifier user', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name_plural': 'orders',
                'verbose_name': 'order',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('identifier', hotelBooking.core.fields.InternalIdentifierField(blank=False, unique=True, editable=False, db_index=True, max_length=64, null=False)),
                ('ordering', models.IntegerField(verbose_name='ordering', db_index=True, default=0)),
                ('role', enumfields.fields.EnumIntegerField(verbose_name='role', db_index=True, default=0, enum=hotelBooking.core.models.orders.OrderStatusRole)),
                ('default', models.BooleanField(verbose_name='default', db_index=True, default=False)),
                ('name', models.CharField(verbose_name='name', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False, editable=False)),
                ('shipping_mode', enumfields.fields.EnumIntegerField(verbose_name='shipping mode', default=0, enum=hotelBooking.core.models.products.ShippingMode)),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('identifier', hotelBooking.core.fields.InternalIdentifierField(blank=True, unique=True, editable=False, max_length=64, null=True)),
            ],
            options={
                'verbose_name_plural': 'product types',
                'verbose_name': 'product type',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('name_py', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': '省份',
                'verbose_name': '省份',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(related_name='product_orders', blank=True, null=True, verbose_name='product', to='hotelBooking.Product', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='status', to='hotelBooking.OrderStatus'),
        ),
        migrations.AddField(
            model_name='housepackage',
            name='product',
            field=models.OneToOneField(to='hotelBooking.Product'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(related_name='citys', verbose_name='所属省份', to='hotelBooking.Province'),
        ),
    ]
