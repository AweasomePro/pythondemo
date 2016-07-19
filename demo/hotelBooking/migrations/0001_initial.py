# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.models.user.users
import django.db.models.deletion
import hotelBooking.utils.fiels
from django.conf import settings
import enumfields.fields
import django.utils.timezone
import jsonfield.fields
import hotelBooking.core.fields.pointField
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20160712_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
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
                ('groups', models.ManyToManyField(verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, to='auth.Group', related_name='user_set', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', help_text='Specific permissions for this user.', blank=True, to='auth.Permission', related_name='user_set', related_query_name='user')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.IntegerField(unique=True, verbose_name='城市代号', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='城市', max_length=200)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('avatar', models.URLField(blank=True)),
                ('last_access', models.DateTimeField(verbose_name='Last accessed', default=django.utils.timezone.now)),
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
                ('active', models.BooleanField(verbose_name='是否可用', default=True)),
                ('modified', models.DateTimeField(verbose_name='State modified', auto_now_add=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='酒店名', max_length=200)),
                ('address', models.CharField(verbose_name='地址', max_length=255)),
                ('introduce', models.TextField(verbose_name='介绍', max_length=255)),
                ('contact_phone', models.CharField(verbose_name='联系电话', max_length=255)),
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
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
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
            name='Installation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=200, default=django.utils.timezone.now)),
                ('channels', hotelBooking.utils.fiels.ListField(null=True, verbose_name='订阅渠道', default=['public', 'private'])),
                ('deviceToken', models.CharField(null=True, max_length=200)),
                ('installationId', models.CharField(null=True, verbose_name='设备id', max_length=200)),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('active', models.BooleanField(verbose_name='active?', default=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True)),
                ('number', models.CharField(unique=True, max_length=30, db_index=True, blank=True)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
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
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('product_name', models.CharField(null=True, help_text='Product name at the moment of purchase', max_length=255, blank=True, verbose_name='Product name')),
                ('product_code', models.CharField(null=True, help_text='Product code at the moment of purchase', max_length=255, blank=True, verbose_name='Product code ')),
            ],
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', enumfields.fields.EnumIntegerField(verbose_name='加盟商类型', default=1, enum=hotelBooking.models.user.users.ProductMemberType)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '加盟会员',
                'verbose_name_plural': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('id', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('unit_price', models.IntegerField(verbose_name='单位价格(元)', default=1)),
                ('number', models.IntegerField(verbose_name='购买的数量')),
                ('total_price', models.FloatField(verbose_name='总价')),
                ('status', models.IntegerField(choices=[(1, '未支付'), (2, '支付成功')], default=1)),
                ('pay_method', models.IntegerField(choices=[(1, '支付宝')], default=1)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', editable=False, default=False, db_index=True)),
                ('type', models.IntegerField(verbose_name='product type', choices=[(1, '酒店订房')], default=1, editable=False)),
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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '省份',
                'verbose_name_plural': '省份',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('checked', models.BooleanField(verbose_name='审核过 ?', default=False)),
                ('active', models.BooleanField(verbose_name='是否可用 ?', default=False)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='房型', max_length=255, default='未定义房型名')),
                ('hotel', models.ForeignKey(verbose_name='所属酒店', to='hotelBooking.Hotel', related_name='hotel_rooms')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '房型',
            },
        ),
        migrations.CreateModel(
            name='RoomDayState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('need_point', models.IntegerField(verbose_name='当天所需积分', default=0)),
                ('front_price', models.IntegerField(verbose_name='当天前台现付价格')),
                ('date', models.DateField()),
                ('state', models.IntegerField(choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')], default=1)),
                ('agent', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(related_name='roomstates', to='hotelBooking.City')),
                ('hotel', models.ForeignKey(related_name='roomstates', to='hotelBooking.Hotel')),
                ('room', models.ForeignKey(to='hotelBooking.Room')),
            ],
            options={
                'verbose_name': '房间类型状态',
                'verbose_name_plural': '房间类型状态',
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='RoomImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('room', models.ForeignKey(verbose_name='房型', to='hotelBooking.Room', related_name='room_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, to='hotelBooking.Order', parent_link=True, primary_key=True, serialize=False)),
                ('checkin_time', models.DateField(verbose_name='入住时间')),
                ('checkout_time', models.DateField(verbose_name='离店时间')),
                ('closed', models.BooleanField(default=False)),
                ('process_state', models.IntegerField(help_text='订单进行的状态', choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (16, '代理接收了订单'), (32, '代理拒绝了订单'), (48, '代理提前表示某些原因导致不能入住了')], default=1)),
                ('total_front_prices', models.IntegerField(verbose_name='total need prices', help_text='所需前台总价')),
                ('total_need_points', models.IntegerField(verbose_name='total need points', help_text='所需积分总和')),
                ('hotel_name', models.CharField(verbose_name='hotel name', help_text='hotel name at the moment of purchase', max_length=255)),
                ('room_name', models.CharField(verbose_name='room name', help_text='room name at the moment of purchase', max_length=255)),
                ('request_notes', models.TextField(null=True, help_text='用户订单要求', blank=True)),
                ('comment', models.TextField(null=True, help_text='消费评价', blank=True)),
                ('guests', jsonfield.fields.JSONField(null=True, help_text='入住人信息', blank=True)),
            ],
            options={
                'permissions': (('change_process_state', '能够操作改变订单过程状态'),),
            },
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HotelPackageOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(auto_created=True, to='hotelBooking.OrderItem', parent_link=True, primary_key=True, serialize=False)),
                ('day', models.DateField(verbose_name='check in day', help_text='日期')),
                ('point', models.IntegerField(verbose_name='need point', help_text='所需积分(moment)')),
                ('front_price', models.IntegerField(verbose_name='front price', help_text='当天前台现付价格(moment)')),
            ],
            bases=('hotelBooking.orderitem',),
        ),
        migrations.CreateModel(
            name='RoomPackage',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, to='hotelBooking.Product', parent_link=True, primary_key=True, serialize=False)),
                ('checked', models.BooleanField(verbose_name='审核过 ?', default=False)),
                ('active', models.BooleanField(verbose_name='是否可用 ?', default=False)),
                ('breakfast', models.IntegerField(verbose_name='早餐类型', choices=[(1, '无早'), (2, '单早'), (3, '双早')], default=1)),
                ('default_point', models.IntegerField(verbose_name='默认所需积分', default=0)),
                ('default_front_price', models.IntegerField(verbose_name='默认前台现付价格')),
                ('extra', jsonfield.fields.JSONField(null=True, help_text='Arbitrary information for this roompackage object.', blank=True, verbose_name='Extra fields')),
                ('hotel', models.ForeignKey(verbose_name='酒店', to='hotelBooking.Hotel')),
                ('room', models.ForeignKey(verbose_name='房型', to='hotelBooking.Room', related_name='roomPackages')),
            ],
            options={
                'verbose_name': '套餐',
                'verbose_name_plural': '套餐',
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
            field=models.ForeignKey(verbose_name='Order', to='hotelBooking.Order', related_name='items'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, verbose_name='Product', to='hotelBooking.Product', on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(verbose_name='customer', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, related_name='customer_orders', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(null=True, verbose_name='modifier user', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, related_name='orders_modified', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(verbose_name='product', on_delete=django.db.models.deletion.PROTECT, to='hotelBooking.Product', related_name='product_orders', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='seller_orders', blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(verbose_name='所属省份', to='hotelBooking.Province', related_name='citys'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='roomPackage',
            field=models.ForeignKey(related_name='roomstates', to='hotelBooking.RoomPackage'),
        ),
    ]
