# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.core.models.orders
import hotelBooking.core.models.products
import hotelBooking.core.fields.pointField
import hotelBooking.utils.fiels
import hotelBooking.core.models.user
from django.conf import settings
import django.db.models.deletion
import hotelBooking.core.fields
import enumfields.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(editable=False, verbose_name='积分', default=0)),
                ('groups', models.ManyToManyField(default=None, blank=True, to='auth.Group')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.IntegerField(verbose_name='城市代号', unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='城市')),
                ('name_py', models.CharField(max_length=200, verbose_name='城市拼音')),
                ('logo', models.URLField(verbose_name='城市Logo图', default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('avatar', models.URLField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '会员',
                'verbose_name_plural': '会员',
            },
        ),
        migrations.CreateModel(
            name='FranchiseeMember',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('type', enumfields.fields.EnumIntegerField(default=1, verbose_name='加盟商类型', enum=hotelBooking.core.models.user.ProductMemberType)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '加盟会员',
                'verbose_name_plural': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='酒店名')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('introduce', models.TextField(max_length=255, verbose_name='介绍')),
                ('contact_phone', models.CharField(max_length=255, verbose_name='联系电话')),
                ('city', models.ForeignKey(related_name='hotels', verbose_name='所在城市', to='hotelBooking.City')),
            ],
            options={
                'verbose_name': '酒店',
                'verbose_name_plural': '酒店',
            },
        ),
        migrations.CreateModel(
            name='HotelImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(max_length=250, verbose_name='图片地址')),
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
                ('name', models.CharField(max_length=255, verbose_name='房型', default='未定义房型名')),
                ('hotel', models.ForeignKey(related_name='hotel_houses', verbose_name='所属酒店', to='hotelBooking.Hotel')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '房型',
            },
        ),
        migrations.CreateModel(
            name='HouseImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(max_length=250, verbose_name='图片地址')),
                ('house', models.ForeignKey(related_name='house_Imgs', verbose_name='房型', to='hotelBooking.House')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousePackage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('package_name', models.CharField(max_length=255, verbose_name='套餐名', default='套餐名')),
                ('need_point', models.IntegerField(verbose_name='所需积分')),
                ('package_state', models.CharField(choices=[('1', '充沛'), ('2', '满房')], max_length=255, default='充沛')),
                ('detail', models.TextField()),
                ('house', models.ForeignKey(related_name='housePackages', verbose_name='房型', to='hotelBooking.House')),
            ],
            options={
                'verbose_name': '套餐',
                'verbose_name_plural': '套餐',
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('badge', models.BigIntegerField(default=0, verbose_name='ios badge数')),
                ('channels', hotelBooking.utils.fiels.ListField(default=[], verbose_name='订阅渠道')),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('deviceToken', models.CharField(max_length=200, null=True, unique=True)),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('installationId', models.CharField(max_length=200, verbose_name='设备id', null=True, unique=True)),
                ('timeZone', models.CharField(max_length=200, null=True, default=django.utils.timezone.now)),
                ('user', models.ForeignKey(verbose_name='绑定用户', null=True, default=-1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'App已安装设备',
                'verbose_name_plural': '设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
                ('identifier', hotelBooking.core.fields.InternalIdentifierField(db_index=True, editable=False, blank=True, null=True, unique=True, max_length=64)),
                ('label', models.CharField(db_index=True, max_length=32, verbose_name='label')),
                ('key', models.CharField(max_length=32, verbose_name='key', unique=True)),
                ('reference_number', models.CharField(db_index=True, max_length=64, verbose_name='reference number', blank=True, null=True, unique=True)),
                ('deleted', models.BooleanField(db_index=True, default=False, verbose_name='deleted')),
                ('payment_status', enumfields.fields.EnumIntegerField(db_index=True, verbose_name='payment status', enum=hotelBooking.core.models.orders.PaymentStatus, default=0)),
                ('shipping_status', enumfields.fields.EnumIntegerField(db_index=True, verbose_name='shipping status', enum=hotelBooking.core.models.orders.ShippingStatus, default=0)),
                ('customer', models.ForeignKey(related_name='customer_orders', verbose_name='customer', blank=True, null=True, to='hotelBooking.CustomerMember', on_delete=django.db.models.deletion.PROTECT)),
                ('modified_by', models.ForeignKey(related_name='orders_modified', verbose_name='modifier user', blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'order',
                'ordering': ('-id',),
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', hotelBooking.core.fields.InternalIdentifierField(db_index=True, editable=False, blank=False, null=False, unique=True, max_length=64)),
                ('ordering', models.IntegerField(db_index=True, default=0, verbose_name='ordering')),
                ('role', enumfields.fields.EnumIntegerField(db_index=True, verbose_name='role', enum=hotelBooking.core.models.orders.OrderStatusRole, default=0)),
                ('default', models.BooleanField(db_index=True, default=False, verbose_name='default')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(db_index=True, editable=False, verbose_name='deleted', default=False)),
                ('shipping_mode', enumfields.fields.EnumIntegerField(default=0, verbose_name='shipping mode', enum=hotelBooking.core.models.products.ShippingMode)),
                ('owner', models.ForeignKey(to='hotelBooking.FranchiseeMember')),
            ],
            options={
                'verbose_name': 'product',
                'ordering': ('-id',),
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('identifier', hotelBooking.core.fields.InternalIdentifierField(editable=False, blank=True, null=True, unique=True, max_length=64)),
            ],
            options={
                'verbose_name': 'product type',
                'verbose_name_plural': 'product types',
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
                'verbose_name': '省份',
                'verbose_name_plural': '省份',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(editable=False, verbose_name='product type', to='hotelBooking.ProductType'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(related_name='product_orders', verbose_name='product', blank=True, null=True, to='hotelBooking.Product', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(verbose_name='status', to='hotelBooking.OrderStatus', on_delete=django.db.models.deletion.PROTECT),
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
