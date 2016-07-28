# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import hotelBooking.models.counters
import jsonfield.fields
import django.db.models.deletion
import model_utils.fields
import uuid
import hotelBooking.utils.fiels
import enumfields.fields
import hotelBooking.core.fields.pointField
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20160712_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('sex', models.IntegerField(choices=[(1, 'male'), (0, 'female')], default=1)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('role', models.IntegerField(help_text='该账号的角色标识', choices=[(1, '顾客'), (2, '酒店代理合作伙伴')], default=1)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(default=0, verbose_name='积分', editable=False)),
            ],
            options={
                'verbose_name_plural': '用户',
                'verbose_name': '用户',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.IntegerField(primary_key=True, verbose_name='城市代号', serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='城市')),
                ('logo', models.URLField(default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg', verbose_name='城市Logo图')),
            ],
            options={
                'verbose_name_plural': '城市',
                'verbose_name': '城市',
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', enumfields.fields.EnumIntegerField(primary_key=True, enum=hotelBooking.models.counters.CounterType, verbose_name='identifier', serialize=False)),
                ('value', models.IntegerField(default=0, verbose_name='value')),
            ],
            options={
                'verbose_name_plural': 'counters',
                'verbose_name': 'counter',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('modified', models.DateTimeField(auto_now_add=True, verbose_name='State modified')),
                ('id', models.AutoField(primary_key=True, serialize=False, editable=False)),
                ('name', models.CharField(max_length=200, verbose_name='酒店名')),
                ('smoking', models.BooleanField(default=False, verbose_name='can smoke ')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('introduce', models.TextField(max_length=255, verbose_name='介绍')),
                ('contact_phone', models.CharField(max_length=255, verbose_name='联系电话')),
                ('cover_img', models.ImageField(verbose_name='封面图片', upload_to='')),
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
                ('img', models.ImageField(verbose_name='图片', upload_to='')),
                ('hotel', models.ForeignKey(verbose_name='房型', related_name='hotel_imgs', to='hotelBooking.Hotel')),
            ],
            options={
                'verbose_name': '房间展示图片',
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=200, default=django.utils.timezone.now)),
                ('channels', hotelBooking.utils.fiels.ListField(null=True, default=['public', 'private'], verbose_name='订阅渠道')),
                ('deviceToken', models.CharField(max_length=200, null=True)),
                ('installationId', models.CharField(max_length=200, null=True, verbose_name='设备id')),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('badge', models.BigIntegerField(default=0, verbose_name='ios badge数')),
                ('deviceProfile', models.CharField(max_length=200, default='')),
                ('active', models.BooleanField(default=True, verbose_name='active?')),
            ],
            options={
                'verbose_name_plural': '设备',
                'verbose_name': 'App已安装设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('number', models.CharField(max_length=64, primary_key=True, blank=True, unique=True, serialize=False, db_index=True, editable=False)),
                ('deleted', models.BooleanField(db_index=True, default=False, verbose_name='deleted')),
                ('payment_status', models.IntegerField(choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')], default=1, db_index=True, verbose_name='payment status')),
                ('shipping_status', models.IntegerField(choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')], default=0, db_index=True, verbose_name='shipping status')),
            ],
            options={
                'verbose_name_plural': 'orders',
                'ordering': ('modified',),
                'verbose_name': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('product_name', models.CharField(max_length=255, help_text='Product name at the moment of purchase', null=True, verbose_name='Product name', blank=True)),
                ('product_code', models.CharField(max_length=255, help_text='Product default_code at the moment of purchase', null=True, verbose_name='Product default_code ', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('trade_no', models.CharField(max_length=32, db_index=True, editable=False)),
                ('unit_price', models.PositiveIntegerField(default=1, verbose_name='单位价格(元)')),
                ('number', models.PositiveIntegerField(verbose_name='购买的数量')),
                ('total_price', models.FloatField(verbose_name='总价')),
                ('status', models.IntegerField(choices=[(1, '未支付'), (2, '支付成功')], default=1)),
                ('pay_method', models.IntegerField(choices=[(1, '支付宝')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='create on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='modified on')),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False, editable=False)),
                ('type', models.IntegerField(choices=[(1, '酒店订房')], default=1, verbose_name='product type', editable=False)),
            ],
            options={
                'verbose_name_plural': '产品（数据库基类）',
                'ordering': ('-id',),
                'verbose_name': '产品（数据库基类）',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, editable=False)),
                ('name', models.CharField(max_length=255, default='未定义房型名', verbose_name='房型')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('s_point', models.PositiveIntegerField(default=0, verbose_name='当天单人所需积分')),
                ('s_price', models.PositiveIntegerField(verbose_name='当天单人前台现付价格')),
                ('d_point', models.PositiveIntegerField(default=0, verbose_name='当天双人所需积分')),
                ('d_price', models.PositiveIntegerField(verbose_name='当天双人前台现付价格')),
                ('date', models.DateField()),
                ('state', models.IntegerField(choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')], default=1)),
            ],
            options={
                'verbose_name_plural': '房间类型状态',
                'get_latest_by': 'date',
                'ordering': ('agent', 'date'),
                'verbose_name': '房间类型状态',
            },
        ),
        migrations.CreateModel(
            name='RoomImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(verbose_name='图片', upload_to='')),
                ('room', models.ForeignKey(verbose_name='房型', related_name='room_imgs', to='hotelBooking.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('avatar', models.URLField(blank=True)),
                ('last_access', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last accessed')),
            ],
            options={
                'verbose_name_plural': '会员',
                'verbose_name': '会员',
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order', models.OneToOneField(primary_key=True, to='hotelBooking.Order', serialize=False)),
                ('checkin_time', models.DateField(verbose_name='入住时间')),
                ('checkout_time', models.DateField(verbose_name='离店时间')),
                ('closed', models.BooleanField(default=False)),
                ('process_state', models.IntegerField(help_text='订单进行的状态', choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了')], default=1)),
                ('total_front_prices', models.IntegerField(help_text='所需前台总价', verbose_name='total need prices')),
                ('total_need_points', models.IntegerField(help_text='所需积分总和', verbose_name='total need points')),
                ('breakfast', models.IntegerField(help_text=' 订单生成时,所记录的早餐类型', default=1, verbose_name='早餐类型')),
                ('hotel_name', models.CharField(max_length=255, help_text='hotel name at the moment of purchase', verbose_name='hotel name')),
                ('room_name', models.CharField(max_length=255, help_text='room name at the moment of purchase', verbose_name='room name')),
                ('request_notes', models.TextField(help_text='用户订单要求', null=True, blank=True)),
                ('room_count', models.SmallIntegerField(default=1, verbose_name='房间件数')),
                ('people_count', models.SmallIntegerField(default=1, verbose_name='入住人数')),
                ('comment', models.TextField(help_text='消费评价', null=True, blank=True)),
                ('guests', jsonfield.fields.JSONField(help_text='入住人信息', null=True, blank=True)),
            ],
            options={
                'permissions': (('change_process_state', '能够操作改变订单过程状态'),),
            },
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HotelPackageOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='hotelBooking.OrderItem', auto_created=True)),
                ('day', models.DateField(help_text='日期', verbose_name='check in day')),
                ('point', models.IntegerField(help_text='所需积分(moment)', verbose_name='need point')),
                ('price', models.IntegerField(help_text='当天前台现付价格(moment)', verbose_name='front price')),
            ],
            bases=('hotelBooking.orderitem',),
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
            ],
            options={
                'verbose_name_plural': '加盟会员',
                'verbose_name': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='RoomPackage',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='hotelBooking.Product', auto_created=True)),
                ('checked', models.BooleanField(default=False, verbose_name='审核过 ?')),
                ('active', models.BooleanField(default=False, verbose_name='是否可用 ?')),
                ('breakfast', models.IntegerField(choices=[(1, '无早'), (2, '单早'), (3, '双早')], default=1, verbose_name='早餐类型')),
                ('bill', models.BooleanField(default=True, verbose_name='提供发票')),
                ('price_type', models.IntegerField(choices=[(1, '单双同价'), (2, '单双异价')], default=1, verbose_name='价格类型')),
                ('default_s_point', models.PositiveIntegerField(default=0, verbose_name='默认单人所需积分')),
                ('default_s_price', models.PositiveIntegerField(verbose_name='默认单人现付价格')),
                ('default_d_point', models.PositiveIntegerField(default=0, verbose_name='默认双人所需积分')),
                ('default_d_price', models.PositiveIntegerField(verbose_name='默认双人现付价格')),
                ('extra', jsonfield.fields.JSONField(help_text='Arbitrary information for this roompackage object.', null=True, verbose_name='Extra fields', blank=True)),
            ],
            options={
                'verbose_name_plural': '套餐',
                'verbose_name': '套餐',
            },
            bases=('hotelBooking.product', models.Model),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='agent',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='city',
            field=models.ForeignKey(to='hotelBooking.City', related_name='roomstates'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='hotel',
            field=models.ForeignKey(to='hotelBooking.Hotel', related_name='roomstates'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='room',
            field=models.ForeignKey(to='hotelBooking.Room'),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pay',
            name='user',
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
            field=models.ForeignKey(verbose_name='Product', blank=True, to='hotelBooking.Product', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, related_name='customer_orders', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, verbose_name='customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(verbose_name='modifier user', blank=True, related_name='orders_modified', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, related_name='product_orders', to='hotelBooking.Product', on_delete=django.db.models.deletion.PROTECT, verbose_name='product'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, related_name='seller_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='installation',
            name='user',
            field=models.ForeignKey(to_field='phone_number', verbose_name='绑定用户', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotel',
            name='agent',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(verbose_name='所在城市', related_name='hotels', to='hotelBooking.City'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(verbose_name='所属省份', related_name='citys', to='hotelBooking.Province'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', verbose_name='groups', blank=True, related_name='user_set', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', verbose_name='user permissions', blank=True, related_name='user_set', to='auth.Permission'),
        ),
        migrations.AddField(
            model_name='roompackage',
            name='hotel',
            field=models.ForeignKey(to='hotelBooking.Hotel', verbose_name='酒店'),
        ),
        migrations.AddField(
            model_name='roompackage',
            name='room',
            field=models.ForeignKey(verbose_name='房型', related_name='roomPackages', to='hotelBooking.Room'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='roomPackage',
            field=models.ForeignKey(to='hotelBooking.RoomPackage', related_name='roomstates'),
        ),
        migrations.CreateModel(
            name='ClosedHotelPackageOrder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('hotelBooking.hotelpackageorder',),
        ),
    ]
