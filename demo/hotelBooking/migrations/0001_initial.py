# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.utils.timezone
import hotelBooking.models.user.users
import django.db.models.deletion
from django.conf import settings
import enumfields.fields
import hotelBooking.utils.fiels
import hotelBooking.core.fields.pointField


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('sex', models.IntegerField(default=1, choices=[(1, 'male'), (0, 'female')])),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(verbose_name='积分', default=0, editable=False)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', verbose_name='groups', related_name='user_set', blank=True, to='auth.Group')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', verbose_name='user permissions', related_name='user_set', blank=True, to='auth.Permission')),
            ],
            options={
                'verbose_name_plural': '用户',
                'verbose_name': '用户',
            },
            bases=(hotelBooking.models.user.users.PointMixin, models.Model),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.IntegerField(verbose_name='城市代号', serialize=False, unique=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='城市')),
                ('logo', models.URLField(verbose_name='城市Logo图', default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg')),
            ],
            options={
                'verbose_name_plural': '城市',
                'verbose_name': '城市',
            },
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('avatar', models.URLField(blank=True)),
                ('last_access', models.DateTimeField(verbose_name='Last accessed', default=django.utils.timezone.now)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '会员',
                'verbose_name': '会员',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('id', models.AutoField(serialize=False, primary_key=True, editable=False)),
                ('name', models.CharField(max_length=200, verbose_name='酒店名')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('introduce', models.TextField(max_length=255, verbose_name='介绍')),
                ('contact_phone', models.CharField(max_length=255, verbose_name='联系电话')),
                ('agent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(verbose_name='所在城市', related_name='hotels', to='hotelBooking.City')),
            ],
            options={
                'verbose_name_plural': '酒店',
                'verbose_name': '酒店',
            },
        ),
        migrations.CreateModel(
            name='HotelImg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img_url', models.CharField(max_length=250, verbose_name='图片地址')),
                ('hotel', models.ForeignKey(verbose_name='房型', related_name='hotel_imgs', to='hotelBooking.Hotel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=200, default=django.utils.timezone.now)),
                ('channels', hotelBooking.utils.fiels.ListField(verbose_name='订阅渠道', default=['public', 'private'], null=True)),
                ('deviceToken', models.CharField(max_length=200, null=True)),
                ('installationId', models.CharField(max_length=200, verbose_name='设备id', null=True)),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('active', models.BooleanField(default=True, verbose_name='active?')),
                ('user', models.ForeignKey(null=True, verbose_name='绑定用户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '设备',
                'verbose_name': 'App已安装设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True)),
                ('number', models.CharField(max_length=30, blank=True, unique=True, db_index=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('modified_on', models.DateTimeField(auto_now_add=True, verbose_name='modified on')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted', db_index=True)),
                ('payment_status', models.IntegerField(verbose_name='payment status', db_index=True, default=1, choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')])),
                ('shipping_status', models.IntegerField(verbose_name='shipping status', db_index=True, default=0, choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')])),
            ],
            options={
                'verbose_name_plural': 'orders',
                'verbose_name': 'order',
                'ordering': ('created_on',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('product_name', models.CharField(verbose_name='Product name', max_length=255, help_text='Product name at the moment of purchase', null=True, blank=True)),
                ('product_code', models.CharField(verbose_name='Product code ', max_length=255, help_text='Product code at the moment of purchase', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('type', enumfields.fields.EnumIntegerField(enum=hotelBooking.models.user.users.ProductMemberType, verbose_name='加盟商类型', default=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '加盟会员',
                'verbose_name': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='create on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='modified on')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted', editable=False, db_index=True)),
                ('type', models.IntegerField(verbose_name='product type', default=1, editable=False, choices=[(1, '酒店订房')])),
            ],
            options={
                'verbose_name_plural': '产品（数据库基类）',
                'verbose_name': '产品（数据库基类）',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': '省份',
                'verbose_name': '省份',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('checked', models.BooleanField(default=False, verbose_name='审核过 ?')),
                ('active', models.BooleanField(default=False, verbose_name='是否可用 ?')),
                ('id', models.AutoField(serialize=False, primary_key=True, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='房型', default='未定义房型名')),
                ('hotel', models.ForeignKey(verbose_name='所属酒店', related_name='hotel_rooms', to='hotelBooking.Hotel')),
            ],
            options={
                'verbose_name_plural': '房型',
                'verbose_name': '房型',
            },
        ),
        migrations.CreateModel(
            name='RoomDayState',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('need_point', models.IntegerField(verbose_name='当天所需积分', default=0)),
                ('front_price', models.IntegerField(verbose_name='当天前台现付价格')),
                ('date', models.DateField()),
                ('state', models.IntegerField(default=1, choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')])),
                ('agent', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(to='hotelBooking.City', related_name='city_roomstates')),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', related_name='hotel_roomstates')),
                ('room', models.ForeignKey(to='hotelBooking.Room')),
            ],
            options={
                'verbose_name_plural': '房间类型状态',
                'get_latest_by': 'date',
                'verbose_name': '房间类型状态',
            },
        ),
        migrations.CreateModel(
            name='RoomImg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img_url', models.CharField(max_length=250, verbose_name='图片地址')),
                ('room', models.ForeignKey(verbose_name='房型', related_name='room_imgs', to='hotelBooking.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(to='hotelBooking.Order', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('checkin_time', models.DateField(verbose_name='入住时间')),
                ('checkout_time', models.DateField(verbose_name='离店时间')),
                ('closed', models.BooleanField(default=False)),
                ('process_state', models.IntegerField(help_text='订单进行的状态', default=1, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (16, '代理接收了订单'), (32, '代理拒绝了订单'), (48, '代理提前表示某些原因导致不能入住了')])),
                ('total_front_prices', models.IntegerField(help_text='所需前台总价', verbose_name='total need prices')),
                ('total_need_points', models.IntegerField(help_text='所需积分总和', verbose_name='total need points')),
                ('hotel_name', models.CharField(max_length=255, help_text='hotel name at the moment of purchase', verbose_name='hotel name')),
                ('room_name', models.CharField(max_length=255, help_text='room name at the moment of purchase', verbose_name='room name')),
                ('request_notes', models.TextField(help_text='用户订单要求', null=True, blank=True)),
                ('comment', models.TextField(help_text='消费评价', null=True, blank=True)),
            ],
            options={
                'permissions': (('change_process_state', '能够操作改变订单过程状态'),),
            },
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HotelPackageOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(to='hotelBooking.OrderItem', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('day', models.DateField(help_text='日期', verbose_name='check in day')),
                ('point', models.IntegerField(help_text='所需积分(moment)', verbose_name='need point')),
                ('front_price', models.IntegerField(help_text='当天前台现付价格(moment)', verbose_name='front price')),
            ],
            bases=('hotelBooking.orderitem',),
        ),
        migrations.CreateModel(
            name='RoomPackage',
            fields=[
                ('product_ptr', models.OneToOneField(to='hotelBooking.Product', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('checked', models.BooleanField(default=False, verbose_name='审核过 ?')),
                ('active', models.BooleanField(default=False, verbose_name='是否可用 ?')),
                ('breakfast', models.IntegerField(verbose_name='早餐类型', default=1, choices=[(1, '无早'), (2, '单早'), (3, '双早')])),
                ('default_point', models.IntegerField(verbose_name='默认所需积分', default=0)),
                ('default_front_price', models.IntegerField(verbose_name='默认前台现付价格')),
                ('detail', models.TextField(blank=True, default='')),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', verbose_name='酒店')),
                ('room', models.ForeignKey(verbose_name='房型', related_name='roomPackages', to='hotelBooking.Room')),
            ],
            options={
                'verbose_name_plural': '套餐',
                'verbose_name': '套餐',
            },
            bases=('hotelBooking.product', models.Model),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(verbose_name='Order', related_name='items', to='hotelBooking.Order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='Product', to='hotelBooking.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, related_name='customer_orders', on_delete=django.db.models.deletion.PROTECT, verbose_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(blank=True, related_name='orders_modified', null=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='modifier user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, related_name='product_orders', on_delete=django.db.models.deletion.PROTECT, verbose_name='product', to='hotelBooking.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, related_name='seller_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(verbose_name='所属省份', related_name='citys', to='hotelBooking.Province'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='roomPackage',
            field=models.ForeignKey(to='hotelBooking.RoomPackage', related_name='roompackage_daystates'),
        ),
    ]
