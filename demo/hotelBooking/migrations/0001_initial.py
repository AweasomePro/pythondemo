# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid
import hotelBooking.utils.fiels
import hotelBooking.core.models.user
import hotelBooking.core.fields.pointField
import enumfields.fields
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(default='unknow name', max_length=225)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('sex', models.IntegerField(default=1, choices=[(1, 'male'), (0, 'female')])),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(default=0, verbose_name='积分', editable=False)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='AgentRoomTypeState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
                ('code', models.IntegerField(verbose_name='城市代号', serialize=False, primary_key=True, unique=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
                ('name', models.CharField(max_length=200, verbose_name='酒店名')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('introduce', models.TextField(max_length=255, verbose_name='介绍')),
                ('contact_phone', models.CharField(max_length=255, verbose_name='联系电话')),
                ('agent', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(verbose_name='所在城市', to='hotelBooking.City', related_name='hotels')),
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
                ('hotel', models.ForeignKey(verbose_name='房型', to='hotelBooking.Hotel', related_name='hotel_imgs')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
                ('name', models.CharField(default='未定义房型名', max_length=255, verbose_name='房型')),
                ('hotel', models.ForeignKey(verbose_name='所属酒店', to='hotelBooking.Hotel', related_name='hotel_houses')),
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
                ('house', models.ForeignKey(verbose_name='房型', to='hotelBooking.House', related_name='house_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(default=django.utils.timezone.now, max_length=200)),
                ('channels', hotelBooking.utils.fiels.ListField(default=['public', 'private'], null=True, verbose_name='订阅渠道')),
                ('deviceToken', models.CharField(max_length=200, null=True)),
                ('installationId', models.CharField(max_length=200, null=True, verbose_name='设备id')),
                ('deviceType', models.CharField(default='android', max_length=200)),
                ('badge', models.BigIntegerField(default=0, verbose_name='ios badge数')),
                ('deviceProfile', models.CharField(default='', max_length=200)),
                ('user', models.ForeignKey(null=True, verbose_name='绑定用户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'App已安装设备',
                'verbose_name_plural': '设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('number', models.CharField(max_length=30, db_index=True, blank=True, unique=True)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
                ('label', models.CharField(max_length=32, verbose_name='label', db_index=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted', db_index=True)),
                ('payment_status', models.IntegerField(default=1, verbose_name='payment status', choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')], db_index=True)),
                ('shipping_status', models.IntegerField(default=0, verbose_name='shipping status', choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')], db_index=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('type', enumfields.fields.EnumIntegerField(default=1, verbose_name='加盟商类型', enum=hotelBooking.core.models.user.ProductMemberType)),
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='modified on')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted', editable=False, db_index=True)),
                ('type', models.IntegerField(default=1, verbose_name='product type', choices=[(1, '酒店订房')])),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, to='hotelBooking.Order', auto_created=True, primary_key=True, serialize=False)),
                ('check_in_time', models.DateField(verbose_name='入住时间')),
                ('check_out_time', models.DateField(verbose_name='离店时间')),
                ('process_state', models.IntegerField(default=1, help_text='订单进行的状态', choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (16, '代理接收了订单'), (32, '代理拒绝了订单'), (48, '代理提前表示某些原因导致不能入住了')])),
                ('require_notes', models.TextField(null=True, blank=True)),
                ('closed', models.BooleanField(default=False)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HousePackage',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, to='hotelBooking.Product', auto_created=True, primary_key=True, serialize=False)),
                ('need_point', models.IntegerField(default=0, verbose_name='所需积分')),
                ('front_price', models.IntegerField(verbose_name='前台现付价格')),
                ('detail', models.TextField()),
                ('house', models.ForeignKey(verbose_name='房型', to='hotelBooking.House', related_name='housePackages')),
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
            field=models.ForeignKey(verbose_name='customer', on_delete=django.db.models.deletion.PROTECT, related_name='customer_orders', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(null=True, verbose_name='modifier user', on_delete=django.db.models.deletion.PROTECT, related_name='orders_modified', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(verbose_name='product', on_delete=django.db.models.deletion.PROTECT, related_name='product_orders', to='hotelBooking.Product', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='seller_orders'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(verbose_name='所属省份', to='hotelBooking.Province', related_name='citys'),
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
