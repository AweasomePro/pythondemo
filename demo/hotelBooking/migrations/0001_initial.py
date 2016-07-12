# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
import hotelBooking.utils.fiels
import hotelBooking.core.models.user
import hotelBooking.core.fields.pointField
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import hotelBooking.models
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20160712_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('phone_number', models.CharField(unique=True, max_length=15)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('sex', models.IntegerField(choices=[(1, 'male'), (0, 'female')], default=1)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(verbose_name='积分', default=0, editable=False)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            bases=(hotelBooking.models.PointMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AgentRoomTypeState',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateField()),
                ('state', models.IntegerField(choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')], default=1)),
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
                ('code', models.IntegerField(unique=True, verbose_name='城市代号', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='城市')),
                ('name_py', models.CharField(max_length=200, verbose_name='城市拼音')),
                ('logo', models.URLField(default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg', verbose_name='城市Logo图')),
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
            name='Hotel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='酒店名')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('introduce', models.TextField(max_length=255, verbose_name='介绍')),
                ('contact_phone', models.CharField(max_length=255, verbose_name='联系电话')),
                ('agent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(to='hotelBooking.City', verbose_name='所在城市', related_name='hotels')),
            ],
            options={
                'verbose_name': '酒店',
                'verbose_name_plural': '酒店',
            },
        ),
        migrations.CreateModel(
            name='HotelImg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img_url', models.CharField(max_length=250, verbose_name='图片地址')),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', verbose_name='房型', related_name='hotel_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='HotelPackageOrderSnapShot',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, default='未定义房型名', verbose_name='房型')),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', verbose_name='所属酒店', related_name='hotel_houses')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '房型',
            },
        ),
        migrations.CreateModel(
            name='HouseImg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img_url', models.CharField(max_length=250, verbose_name='图片地址')),
                ('house', models.ForeignKey(to='hotelBooking.House', verbose_name='房型', related_name='house_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=200, default=django.utils.timezone.now)),
                ('channels', hotelBooking.utils.fiels.ListField(verbose_name='订阅渠道', null=True, default=['public', 'private'])),
                ('deviceToken', models.CharField(max_length=200, null=True)),
                ('installationId', models.CharField(max_length=200, null=True, verbose_name='设备id')),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='绑定用户', null=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('number', models.CharField(unique=True, max_length=30, blank=True, db_index=True)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
                ('label', models.CharField(max_length=32, db_index=True, verbose_name='label')),
                ('deleted', models.BooleanField(verbose_name='deleted', default=False, db_index=True)),
                ('payment_status', models.IntegerField(verbose_name='payment status', choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')], default=1, db_index=True)),
                ('shipping_status', models.IntegerField(verbose_name='shipping status', choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')], default=0, db_index=True)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('created_on',),
            },
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('type', enumfields.fields.EnumIntegerField(verbose_name='加盟商类型', default=1, enum=hotelBooking.core.models.user.ProductMemberType)),
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
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False, editable=False)),
                ('type', models.IntegerField(verbose_name='product type', choices=[(1, '酒店订房')], default=1)),
            ],
            options={
                'verbose_name': '产品（数据库基类）',
                'verbose_name_plural': '产品（数据库基类）',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(serialize=False, parent_link=True, to='hotelBooking.Order', primary_key=True, auto_created=True)),
                ('checkin_time', models.DateField(verbose_name='入住时间')),
                ('checkout_time', models.DateField(verbose_name='离店时间')),
                ('process_state', models.IntegerField(help_text='订单进行的状态', choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (16, '代理接收了订单'), (32, '代理拒绝了订单'), (48, '代理提前表示某些原因导致不能入住了')], default=1)),
                ('request_notes', models.TextField(blank=True, null=True)),
                ('closed', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
            options={
                'permissions': (('change_process_state', '能够操作改变订单过程状态'),),
            },
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HousePackage',
            fields=[
                ('product_ptr', models.OneToOneField(serialize=False, parent_link=True, to='hotelBooking.Product', primary_key=True, auto_created=True)),
                ('breakfast', models.IntegerField(verbose_name='breakfast type', choices=[(1, '无早'), (2, '单早'), (3, '双早')], default=1)),
                ('need_point', models.IntegerField(verbose_name='所需积分', default=0)),
                ('front_price', models.IntegerField(verbose_name='前台现付价格')),
                ('detail', models.TextField()),
                ('house', models.ForeignKey(to='hotelBooking.House', verbose_name='房型', related_name='housePackages')),
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='customer', on_delete=django.db.models.deletion.PROTECT, related_name='customer_orders'),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='modifier user', on_delete=django.db.models.deletion.PROTECT, related_name='orders_modified', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='hotelBooking.Product', blank=True, verbose_name='product', on_delete=django.db.models.deletion.PROTECT, related_name='product_orders'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='seller_orders'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='hotelBooking.Province', verbose_name='所属省份', related_name='citys'),
        ),
        migrations.AddField(
            model_name='agentroomtypestate',
            name='city',
            field=models.ForeignKey(related_name='city_roomstates', to='hotelBooking.City'),
        ),
        migrations.AddField(
            model_name='agentroomtypestate',
            name='hotel',
            field=models.ForeignKey(related_name='hotel_roomstates', to='hotelBooking.Hotel'),
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
            field=models.ForeignKey(related_name='housepackage_roomstates', to='hotelBooking.HousePackage'),
        ),
    ]
