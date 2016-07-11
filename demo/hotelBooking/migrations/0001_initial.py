# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.utils.fiels
from django.conf import settings
import hotelBooking.core.fields.pointField
import enumfields.fields
import django.db.models.deletion
import datetime
import hotelBooking.core.models.products
import django.utils.timezone
import hotelBooking.core.models.user
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('sex', models.IntegerField(default=1, choices=[(1, 'male'), (0, 'female')])),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(editable=False, verbose_name='积分', default=0)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True, default=None)),
                ('permissions', models.ManyToManyField(to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='AgentRoomTypeState',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('state', models.IntegerField(default=1, choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')])),
                ('agent', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '房间类型状态',
                'verbose_name_plural': '房间类型状态',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.IntegerField(verbose_name='城市代号', primary_key=True, unique=True, serialize=False)),
                ('name', models.CharField(verbose_name='城市', max_length=200)),
                ('name_py', models.CharField(verbose_name='城市拼音', max_length=200)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('avatar', models.URLField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '会员',
                'verbose_name_plural': '会员',
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
                ('agent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(to='hotelBooking.City', related_name='hotels', verbose_name='所在城市')),
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
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', related_name='hotel_imgs', verbose_name='房型')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='HotelPackageOrderSnapShot',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('hotel_id', models.IntegerField()),
                ('house_id', models.IntegerField()),
                ('hotel_name', models.CharField(max_length=255)),
                ('house_name', models.CharField(max_length=255)),
                ('front_price', models.IntegerField()),
                ('need_point', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='房型', max_length=255, default='未定义房型名')),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', related_name='hotel_houses', verbose_name='所属酒店')),
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
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('house', models.ForeignKey(to='hotelBooking.House', related_name='house_imgs', verbose_name='房型')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=200, default=django.utils.timezone.now)),
                ('channels', hotelBooking.utils.fiels.ListField(verbose_name='订阅渠道', null=True, default=['public', 'private'])),
                ('deviceToken', models.CharField(max_length=200, null=True)),
                ('installationId', models.CharField(verbose_name='设备id', max_length=200, null=True)),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='绑定用户')),
            ],
            options={
                'verbose_name': 'App已安装设备',
                'verbose_name_plural': '设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(editable=False, default=uuid.uuid4)),
                ('number', models.CharField(blank=True, max_length=30, db_index=True, unique=True)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
                ('label', models.CharField(verbose_name='label', max_length=32, db_index=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False)),
                ('payment_status', models.IntegerField(verbose_name='payment status', db_index=True, default=1, choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')])),
                ('shipping_status', models.IntegerField(verbose_name='shipping status', db_index=True, default=0, choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')])),
            ],
            options={
                'ordering': ('created_on',),
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('type', enumfields.fields.EnumIntegerField(verbose_name='加盟商类型', enum=hotelBooking.core.models.user.ProductMemberType, default=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '加盟会员',
                'verbose_name_plural': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(editable=False, verbose_name='deleted', db_index=True, default=False)),
                ('type', models.CharField(verbose_name='product type', max_length=255, default=('hotel_house_package', '酒店订房'), choices=[('hotel_house_package', '酒店订房')])),
                ('shipping_mode', enumfields.fields.EnumIntegerField(verbose_name='shipping mode', enum=hotelBooking.core.models.products.ShippingMode, default=0)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '产品（数据库基类）',
                'verbose_name_plural': '产品（数据库基类）',
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
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(to='hotelBooking.Order', serialize=False, auto_created=True, parent_link=True, primary_key=True)),
                ('check_in_time', models.DateField(verbose_name='入住时间', default=datetime.date(2016, 7, 10))),
                ('check_out_time', models.DateField(verbose_name='离店时间', default=datetime.date(2016, 7, 10))),
                ('process_state', models.IntegerField(help_text='订单进行的状态', default=1, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (16, '代理接收了订单'), (32, '代理拒绝了订单'), (48, '代理提前表示某些原因导致不能入住了')])),
                ('require_notes', models.TextField(blank=True, null=True)),
                ('closed', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HousePackage',
            fields=[
                ('product_ptr', models.OneToOneField(to='hotelBooking.Product', serialize=False, auto_created=True, parent_link=True, primary_key=True)),
                ('need_point', models.IntegerField(verbose_name='所需积分', default=0)),
                ('front_price', models.IntegerField(verbose_name='前台现付价格')),
                ('detail', models.TextField()),
                ('house', models.ForeignKey(to='hotelBooking.House', related_name='housePackages', verbose_name='房型')),
            ],
            options={
                'verbose_name': '套餐',
                'verbose_name_plural': '套餐',
            },
            bases=('hotelBooking.product',),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='customer_orders', on_delete=django.db.models.deletion.PROTECT, verbose_name='customer', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='orders_modified', null=True, verbose_name='modifier user', blank=True, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='hotelBooking.Product', related_name='product_orders', on_delete=django.db.models.deletion.PROTECT, verbose_name='product', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='seller_orders', blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='hotelBooking.Province', related_name='citys', verbose_name='所属省份'),
        ),
        migrations.AddField(
            model_name='agentroomtypestate',
            name='city',
            field=models.ForeignKey(to='hotelBooking.City', related_name='city_roomstates'),
        ),
        migrations.AddField(
            model_name='agentroomtypestate',
            name='hotel',
            field=models.ForeignKey(to='hotelBooking.Hotel', related_name='hotel_roomstates'),
        ),
        migrations.AddField(
            model_name='agentroomtypestate',
            name='house_type',
            field=models.ForeignKey(to='hotelBooking.House'),
        ),
        migrations.AddField(
            model_name='hotelpackageordersnapshot',
            name='hotel_package_order',
            field=models.OneToOneField(to='hotelBooking.HotelPackageOrder'),
        ),
        migrations.AddField(
            model_name='agentroomtypestate',
            name='housePackage',
            field=models.ForeignKey(to='hotelBooking.HousePackage', related_name='housepackage_roomstates'),
        ),
    ]
